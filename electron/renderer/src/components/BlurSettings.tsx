import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import TextField from '@mui/material/TextField';

interface Props {
  disabled: boolean;
  blurIntensity: number;
  blurPasses: number;
  onIntensityChange: (v: number) => void;
  onPassesChange: (v: number) => void;
}

export default function BlurSettings({ disabled, blurIntensity, blurPasses, onIntensityChange, onPassesChange }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2, opacity: disabled ? 0.5 : 1 }}>
      <Typography variant="subtitle2" gutterBottom>Blur Settings (Blur Mode Only)</Typography>

      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="caption" color="text.secondary">Intensity</Typography>
          <Typography variant="caption">{blurIntensity}</Typography>
        </Box>
        <Slider
          disabled={disabled}
          value={blurIntensity}
          min={51}
          max={301}
          step={2}
          onChange={(_, v) => onIntensityChange(v as number)}
          size="small"
        />
      </Box>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="caption" color="text.secondary" sx={{ whiteSpace: 'nowrap' }}>Passes:</Typography>
        <TextField
          type="number"
          size="small"
          disabled={disabled}
          value={blurPasses}
          onChange={(e) => {
            const v = Math.max(1, Math.min(10, parseInt(e.target.value) || 1));
            onPassesChange(v);
          }}
          inputProps={{ min: 1, max: 10 }}
          sx={{ width: 80 }}
        />
        <Typography variant="caption" color="text.secondary">More passes = stronger blur</Typography>
      </Box>
    </Paper>
  );
}
