import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';

interface Props {
  maskType: 'black' | 'blur';
  onChange: (v: 'black' | 'blur') => void;
}

export default function ProcessingMode({ maskType, onChange }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Processing Mode</Typography>
      <RadioGroup value={maskType} onChange={(e) => onChange(e.target.value as 'black' | 'blur')}>
        <FormControlLabel
          value="black"
          control={<Radio size="small" />}
          label="⬛ Black Mask (Recommended for maximum privacy)"
        />
        <FormControlLabel
          value="blur"
          control={<Radio size="small" />}
          label="🌫️ Blur (Intelligent contour-following blur)"
        />
      </RadioGroup>
    </Paper>
  );
}
