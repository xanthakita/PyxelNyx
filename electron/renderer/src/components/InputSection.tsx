import React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import FormLabel from '@mui/material/FormLabel';
import { useLanguage } from '../i18n/LanguageContext';

interface Props {
  inputPath: string;
  mediaType: 'images' | 'videos' | 'both';
  onInputPathChange: (v: string) => void;
  onMediaTypeChange: (v: 'images' | 'videos' | 'both') => void;
}

export default function InputSection({ inputPath, mediaType, onInputPathChange, onMediaTypeChange }: Props) {
  const { t } = useLanguage();

  const handleBrowseFile = async () => {
    const result = await window.electron.browseFile();
    if (!result.canceled && result.filePath) onInputPathChange(result.filePath);
  };

  const handleBrowseFolder = async () => {
    const result = await window.electron.browseFolder();
    if (!result.canceled && result.folderPath) onInputPathChange(result.folderPath);
  };

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>{t.inputSelection}</Typography>
      <Box sx={{ display: 'flex', gap: 1, mb: 1.5 }}>
        <TextField
          size="small"
          fullWidth
          placeholder={t.selectFilePlaceholder}
          value={inputPath}
          onChange={(e) => onInputPathChange(e.target.value)}
        />
        <Button
          variant="outlined"
          size="small"
          onClick={handleBrowseFile}
          sx={{ whiteSpace: 'nowrap', minWidth: 'max-content', fontSize: '0.78rem' }}
        >
          {t.browseFile}
        </Button>
        <Button
          variant="outlined"
          size="small"
          onClick={handleBrowseFolder}
          sx={{ whiteSpace: 'nowrap', minWidth: 'max-content', fontSize: '0.78rem' }}
        >
          {t.browseFolder}
        </Button>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <FormLabel sx={{ fontSize: 13, color: 'text.secondary' }}>{t.folderFilter}</FormLabel>
        <RadioGroup row value={mediaType} onChange={(e) => onMediaTypeChange(e.target.value as typeof mediaType)}>
          <FormControlLabel value="both" control={<Radio size="small" />} label={t.both} />
          <FormControlLabel value="images" control={<Radio size="small" />} label={t.imagesOnly} />
          <FormControlLabel value="videos" control={<Radio size="small" />} label={t.videosOnly} />
        </RadioGroup>
      </Box>
    </Paper>
  );
}
