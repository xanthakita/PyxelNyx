import React, { useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useLanguage } from '../i18n/LanguageContext';


interface Props {
  open: boolean;
  onClose: () => void;
}

export default function HelpDialog({ open, onClose }: Props) {
  const { t } = useLanguage();
  const [tab, setTab] = useState(0);

  return (
    <Dialog open={open} onClose={onClose} onTransitionExited={() => setTab(0)} maxWidth="md" fullWidth>
      <DialogTitle>{t.help} — PyxelNyx</DialogTitle>
      <DialogContent>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
          <Tab label={t.guiUsage} />
          <Tab label={t.cliUsage} />
        </Tabs>
        <Box sx={{ height: 400, overflow: 'auto' }}>
          <Typography
            component="pre"
            variant="body2"
            sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: 12 }}
          >
            {tab === 0 ? t.guiHelp : t.cliHelp}
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>{t.close}</Button>
      </DialogActions>
    </Dialog>
  );
}
