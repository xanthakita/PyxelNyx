import React, { useEffect, useState, useRef } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';

import { apiClient } from './api/client';
import type { AppState, ProcessRequest, StatusColor } from './types';
import { LanguageProvider, useLanguage } from './i18n/LanguageContext';

import InputSection from './components/InputSection';
import ProcessingMode from './components/ProcessingMode';
import BlurSettings from './components/BlurSettings';
import AdvancedSettings from './components/AdvancedSettings';
import OutputSettings from './components/OutputSettings';
import ProgressSection from './components/ProgressSection';
import HelpDialog from './components/HelpDialog';
import SettingsDialog from './components/SettingsDialog';

const theme = createTheme({ palette: { mode: 'dark' } });

const DEFAULT_STATE: AppState = {
  inputPath: '',
  maskType: 'black',
  blurIntensity: 151,
  blurPasses: 3,
  confidence: 0.33,
  modelName: 'yolov8n-seg.pt',
  mediaType: 'both',
  keepAudio: true,
  officerName: '',
  caseNumber: '',
  frameInterval: 1,
  enableSkinDetection: false,
  processing: false,
  jobId: null,
  fileProgress: 0,
  overallProgress: 0,
  currentFileName: '',
  statusMessage: 'Ready to process media files',
  statusColor: 'text.secondary',
};

function AppInner() {
  const { t } = useLanguage();
  const [isInitializing, setIsInitializing] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);
  const [state, setState] = useState<AppState>(DEFAULT_STATE);
  const [helpOpen, setHelpOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const cleanupSseRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    apiClient
      .initialize()
      .then(() => setIsInitializing(false))
      .catch((err) => {
        setInitError(err.message || 'Failed to connect to backend');
        setIsInitializing(false);
      });

    return () => {
      cleanupSseRef.current?.();
      cleanupSseRef.current = null;
    };
  }, []);

  const update = (partial: Partial<AppState>) =>
    setState((prev) => ({ ...prev, ...partial }));

  const setStatus = (message: string, color: StatusColor) =>
    update({ statusMessage: message, statusColor: color });

  const handleProcess = async () => {
    if (!state.inputPath.trim()) {
      setStatus('Please select a file or folder first', 'warning.main');
      return;
    }

    const blurIntensity = state.blurIntensity % 2 === 0 ? state.blurIntensity + 1 : state.blurIntensity;

    const parts = [state.officerName.trim(), state.caseNumber.trim()].filter(Boolean);
    const effectiveSuffix = parts.length > 0 ? '-' + parts.join('-') : '-background';

    const request: ProcessRequest = {
      input_path: state.inputPath,
      mask_type: state.maskType,
      blur_intensity: blurIntensity,
      blur_passes: state.blurPasses,
      confidence: state.confidence,
      model_name: state.modelName,
      media_type: state.mediaType,
      keep_audio: state.keepAudio,
      filename_suffix: effectiveSuffix,
      frame_interval: state.frameInterval,
      enable_skin_detection: state.enableSkinDetection,
    };

    update({
      processing: true,
      fileProgress: 0,
      overallProgress: 0,
      currentFileName: '',
    });
    setStatus('Starting...', 'primary.main');

    try {
      const { job_id } = await apiClient.processMedia(request);
      update({ jobId: job_id });
      setStatus('Processing...', 'primary.main');

      cleanupSseRef.current = apiClient.streamProgress(job_id, {
        onProgress: (evt) => {
          update({ fileProgress: evt.percent, currentFileName: evt.file });
        },
        onFileStart: (evt) => {
          const overall = ((evt.index - 1) / evt.total_files) * 100;
          update({
            overallProgress: overall,
            currentFileName: evt.file,
            fileProgress: 0,
          });
          setStatus(`Processing ${evt.index}/${evt.total_files}: ${evt.file}`, 'primary.main');
        },
        onComplete: (evt) => {
          cleanupSseRef.current = null;
          update({
            processing: false,
            jobId: null,
            fileProgress: 100,
            overallProgress: 100,
          });

          if (evt.cancelled) {
            setStatus('Processing cancelled', 'warning.main');
          } else {
            setStatus(`✓ Processed ${evt.successful}/${evt.total} file(s) successfully`, 'success.main');
            if (evt.total === 1 && evt.successful === 1) {
              window.electron.openFile(evt.output_path);
            }
          }
        },
        onError: (evt) => {
          cleanupSseRef.current = null;
          update({ processing: false, jobId: null });
          setStatus(`Error: ${evt.message}`, 'error.main');
        },
      });
    } catch (err) {
      update({ processing: false, jobId: null });
      setStatus(`Error: ${err instanceof Error ? err.message : String(err)}`, 'error.main');
    }
  };

  const handleCancel = async () => {
    if (state.jobId) {
      setStatus('Cancelling...', 'warning.main');
      await apiClient.cancelJob(state.jobId);
    }
  };

  if (isInitializing) {
    return (
      <Box sx={{ width: '100vw', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 2, backgroundColor: '#1a1a1a' }}>
        <CircularProgress />
        <Typography variant="body1" color="text.secondary">Connecting to backend...</Typography>
      </Box>
    );
  }

  if (initError) {
    return (
      <Box sx={{ width: '100vw', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#1a1a1a' }}>
        <Typography color="error">Error: {initError}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#1a1a1a', overflow: 'auto' }}>
      {/* Header */}
      <Box sx={{ p: 2, pb: 1, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Typography variant="h5" fontWeight="bold">PyxelNyx v3.5</Typography>
          <Typography variant="caption" color="text.secondary">{t.appSubtitle}</Typography>
        </Box>
        <Button
          variant="outlined"
          size="small"
          onClick={() => setSettingsOpen(true)}
          sx={{ whiteSpace: 'nowrap', minWidth: 'max-content', flexShrink: 0 }}
        >
          {t.settings}
        </Button>
      </Box>

      <Divider />

      {/* Main content */}
      <Box sx={{ flex: 1, p: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <InputSection
          inputPath={state.inputPath}
          mediaType={state.mediaType}
          onInputPathChange={(v) => update({ inputPath: v })}
          onMediaTypeChange={(v) => update({ mediaType: v })}
        />

        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
          <ProcessingMode
            maskType={state.maskType}
            onChange={(v) => update({ maskType: v })}
          />
          <BlurSettings
            disabled={state.maskType !== 'blur'}
            blurIntensity={state.blurIntensity}
            blurPasses={state.blurPasses}
            onIntensityChange={(v) => update({ blurIntensity: v })}
            onPassesChange={(v) => update({ blurPasses: v })}
          />
        </Box>

        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
          <AdvancedSettings
            confidence={state.confidence}
            modelName={state.modelName}
            enableSkinDetection={state.enableSkinDetection}
            onConfidenceChange={(v) => update({ confidence: v })}
            onModelChange={(v) => update({ modelName: v })}
            onSkinDetectionChange={(v) => update({ enableSkinDetection: v })}
          />
          <OutputSettings
            officerName={state.officerName}
            caseNumber={state.caseNumber}
            frameInterval={state.frameInterval}
            keepAudio={state.keepAudio}
            onOfficerNameChange={(v) => update({ officerName: v })}
            onCaseNumberChange={(v) => update({ caseNumber: v })}
            onFrameIntervalChange={(v) => {
              const next: Partial<AppState> = { frameInterval: v };
              if (v > 1) next.keepAudio = false;
              update(next);
            }}
            onKeepAudioChange={(v) => update({ keepAudio: v })}
          />
        </Box>

        {/* Action buttons */}
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleProcess}
            disabled={state.processing}
            sx={{ flex: 1, fontSize: '0.9rem', whiteSpace: 'nowrap' }}
          >
            {state.processing ? t.processingBtn : t.processMedia}
          </Button>
          {state.processing && (
            <Button
              variant="outlined"
              color="warning"
              size="large"
              onClick={handleCancel}
              sx={{ whiteSpace: 'nowrap', px: 2 }}
            >
              {t.cancel}
            </Button>
          )}
          <Button
            variant="outlined"
            size="large"
            onClick={() => setHelpOpen(true)}
            sx={{ whiteSpace: 'nowrap', px: 2 }}
          >
            {t.help}
          </Button>
        </Box>

        <ProgressSection
          fileProgress={state.fileProgress}
          overallProgress={state.overallProgress}
          currentFileName={state.currentFileName}
          statusMessage={state.statusMessage}
          statusColor={state.statusColor}
        />
      </Box>

      <HelpDialog open={helpOpen} onClose={() => setHelpOpen(false)} />
      <SettingsDialog open={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </Box>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LanguageProvider>
        <AppInner />
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
