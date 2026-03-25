import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { useLanguage } from '../i18n/LanguageContext';

const MODELS = [
  'yolov8n-seg.pt',
  'yolov8s-seg.pt',
  'yolov8m-seg.pt',
  'yolov8l-seg.pt',
  'yolov8x-seg.pt',
];

interface Props {
  confidence: number;
  modelName: string;
  enableSkinDetection: boolean;
  onConfidenceChange: (v: number) => void;
  onModelChange: (v: string) => void;
  onSkinDetectionChange: (v: boolean) => void;
}

export default function AdvancedSettings({ confidence, modelName, enableSkinDetection, onConfidenceChange, onModelChange, onSkinDetectionChange }: Props) {
  const { t } = useLanguage();

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>{t.advancedSettings}</Typography>

      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="caption" color="text.secondary">{t.confidence}</Typography>
          <Typography variant="caption">{confidence.toFixed(2)}</Typography>
        </Box>
        <Slider
          value={confidence}
          min={0.1}
          max={1.0}
          step={0.01}
          onChange={(_, v) => onConfidenceChange(v as number)}
          size="small"
        />
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>{t.personModel}</Typography>
        <Select
          size="small"
          fullWidth
          value={modelName}
          onChange={(e) => onModelChange(e.target.value)}
        >
          {MODELS.map((m) => (
            <MenuItem key={m} value={m}>{m}</MenuItem>
          ))}
        </Select>
      </Box>

      <FormControlLabel
        control={
          <Checkbox
            size="small"
            checked={enableSkinDetection}
            onChange={(e) => onSkinDetectionChange(e.target.checked)}
          />
        }
        label={
          <Box>
            <Typography variant="body2">{t.enableSkinDetection}</Typography>
            <Typography variant="caption" color="text.secondary">{t.skinDetectionDesc}</Typography>
          </Box>
        }
      />
    </Paper>
  );
}
