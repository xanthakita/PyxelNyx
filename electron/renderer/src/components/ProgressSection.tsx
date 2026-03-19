import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
import type { StatusColor } from '../types';

interface Props {
  fileProgress: number;
  overallProgress: number;
  currentFileName: string;
  statusMessage: string;
  statusColor: StatusColor;
}

export default function ProgressSection({ fileProgress, overallProgress, currentFileName, statusMessage, statusColor }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Processing Progress</Typography>
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 3 }}>
        <Box>
          <Typography variant="caption" color="text.secondary" fontWeight="bold">Individual File Progress</Typography>
          <Typography variant="caption" display="block" color="primary.main" noWrap sx={{ mb: 0.5, minHeight: '20px' }}>{currentFileName}</Typography>
          <Typography variant="caption" display="block" sx={{ mb: 0.5 }}>{Math.round(fileProgress)}%</Typography>
          <LinearProgress variant="determinate" value={fileProgress} />
        </Box>
        <Box>
          <Typography variant="caption" color="text.secondary" fontWeight="bold">Overall Progress (Batch)</Typography>
          <Typography variant="caption" display="block" color="success.main" sx={{ mb: 0.5, mt: '20px' }}>{Math.round(overallProgress)}%</Typography>
          <LinearProgress variant="determinate" value={overallProgress} color="success" />
        </Box>
      </Box>
      <Typography variant="body2" color={statusColor} sx={{ mt: 1.5, textAlign: 'center' }}>
        {statusMessage}
      </Typography>
    </Paper>
  );
}
