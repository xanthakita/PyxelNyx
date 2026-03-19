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

interface Props {
  inputPath: string;
  mediaType: 'images' | 'videos' | 'both';
  onInputPathChange: (v: string) => void;
  onMediaTypeChange: (v: 'images' | 'videos' | 'both') => void;
}

export default function InputSection({ inputPath, mediaType, onInputPathChange, onMediaTypeChange }: Props) {
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
      <Typography variant="subtitle2" gutterBottom>Input Selection</Typography>
      <Box sx={{ display: 'flex', gap: 1, mb: 1.5 }}>
        <TextField
          size="small"
          fullWidth
          placeholder="Select a file or folder..."
          value={inputPath}
          onChange={(e) => onInputPathChange(e.target.value)}
        />
        <Button variant="outlined" size="small" onClick={handleBrowseFile} sx={{ whiteSpace: 'nowrap' }}>
          Browse File
        </Button>
        <Button variant="outlined" size="small" onClick={handleBrowseFolder} sx={{ whiteSpace: 'nowrap' }}>
          Browse Folder
        </Button>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <FormLabel sx={{ fontSize: 13, color: 'text.secondary' }}>Folder filter:</FormLabel>
        <RadioGroup row value={mediaType} onChange={(e) => onMediaTypeChange(e.target.value as typeof mediaType)}>
          <FormControlLabel value="both" control={<Radio size="small" />} label="Both" />
          <FormControlLabel value="images" control={<Radio size="small" />} label="Images Only" />
          <FormControlLabel value="videos" control={<Radio size="small" />} label="Videos Only" />
        </RadioGroup>
      </Box>
    </Paper>
  );
}
