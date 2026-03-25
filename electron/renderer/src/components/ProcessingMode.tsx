import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import { useLanguage } from '../i18n/LanguageContext';

interface Props {
  maskType: 'black' | 'blur';
  onChange: (v: 'black' | 'blur') => void;
}

export default function ProcessingMode({ maskType, onChange }: Props) {
  const { t } = useLanguage();

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>{t.processingMode}</Typography>
      <RadioGroup value={maskType} onChange={(e) => onChange(e.target.value as 'black' | 'blur')}>
        <FormControlLabel
          value="black"
          control={<Radio size="small" />}
          label={`${t.blackMask} (${t.blackMaskDesc})`}
        />
        <FormControlLabel
          value="blur"
          control={<Radio size="small" />}
          label={`${t.blurMode} (${t.blurModeDesc})`}
        />
      </RadioGroup>
    </Paper>
  );
}
