import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { useLanguage } from '../i18n/LanguageContext';
import { LANGUAGE_NAMES, type Language } from '../i18n/translations';

interface Props {
  open: boolean;
  onClose: () => void;
}

const LANGUAGES = Object.entries(LANGUAGE_NAMES) as [Language, string][];

export default function SettingsDialog({ open, onClose }: Props) {
  const { language, setLanguage, t } = useLanguage();

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle>{t.settingsTitle}</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 1 }}>
          <Typography variant="body2" sx={{ minWidth: 70 }}>{t.language}:</Typography>
          <Select
            size="small"
            fullWidth
            value={language}
            onChange={(e) => setLanguage(e.target.value as Language)}
          >
            {LANGUAGES.map(([code, name]) => (
              <MenuItem key={code} value={code}>{name}</MenuItem>
            ))}
          </Select>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>{t.close}</Button>
      </DialogActions>
    </Dialog>
  );
}
