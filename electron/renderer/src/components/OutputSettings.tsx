import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { useLanguage } from '../i18n/LanguageContext';

interface Props {
  filenameSuffix: string;
  frameInterval: number;
  keepAudio: boolean;
  onSuffixChange: (v: string) => void;
  onFrameIntervalChange: (v: number) => void;
  onKeepAudioChange: (v: boolean) => void;
}

export default function OutputSettings({ filenameSuffix, frameInterval, keepAudio, onSuffixChange, onFrameIntervalChange, onKeepAudioChange }: Props) {
  const { t } = useLanguage();
  const audioDisabled = frameInterval > 1;

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>{t.outputSettings}</Typography>

      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>{t.filenameSuffix}</Typography>
        <TextField
          size="small"
          fullWidth
          value={filenameSuffix}
          onChange={(e) => onSuffixChange(e.target.value)}
          placeholder="-background"
          helperText="e.g. -background, -blurred, -processed"
        />
      </Box>

      <Box sx={{ mb: 1.5 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>{t.frameInterval}</Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <TextField
            type="number"
            size="small"
            value={frameInterval}
            onChange={(e) => {
              const v = Math.max(1, Math.min(15, parseInt(e.target.value) || 1));
              onFrameIntervalChange(v);
            }}
            inputProps={{ min: 1, max: 15 }}
            sx={{ width: 80 }}
          />
          <Typography variant="caption" color="text.secondary">{t.frameIntervalDesc}</Typography>
        </Box>
      </Box>

      <FormControlLabel
        control={
          <Checkbox
            size="small"
            checked={keepAudio}
            disabled={audioDisabled}
            onChange={(e) => onKeepAudioChange(e.target.checked)}
          />
        }
        label={
          <Box>
            <Typography variant="body2">{t.keepAudio}</Typography>
            <Typography variant="caption" color={audioDisabled ? 'warning.main' : 'text.secondary'}>
              {audioDisabled ? t.audioDisabledDesc : t.keepAudioDesc}
            </Typography>
          </Box>
        }
      />
    </Paper>
  );
}
