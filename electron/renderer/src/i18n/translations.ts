export type Language = 'en' | 'es' | 'pt' | 'fr' | 'it' | 'tl' | 'zh-TW';

export interface T {
  // Header
  appSubtitle: string;

  // Input Section
  inputSelection: string;
  selectFilePlaceholder: string;
  browseFile: string;
  browseFolder: string;
  folderFilter: string;
  both: string;
  imagesOnly: string;
  videosOnly: string;

  // Processing Mode
  processingMode: string;
  blackMask: string;
  blackMaskDesc: string;
  blurMode: string;
  blurModeDesc: string;

  // Blur Settings
  blurSettings: string;
  intensity: string;
  passes: string;
  morePassesStronger: string;

  // Advanced Settings
  advancedSettings: string;
  confidence: string;
  personModel: string;
  enableSkinDetection: string;
  skinDetectionDesc: string;

  // Output Settings
  outputSettings: string;
  filenameSuffix: string;
  frameInterval: string;
  frameIntervalDesc: string;
  keepAudio: string;
  keepAudioDesc: string;
  audioDisabledDesc: string;

  // Action buttons
  processMedia: string;
  processingBtn: string;
  cancel: string;
  help: string;
  settings: string;

  // Progress
  processingProgress: string;
  individualFileProgress: string;
  overallProgress: string;
  ready: string;

  // Settings Dialog
  settingsTitle: string;
  language: string;
  close: string;

  // Help Dialog tabs
  guiUsage: string;
  cliUsage: string;
}

export const LANGUAGE_NAMES: Record<Language, string> = {
  en: 'English',
  es: 'Español',
  pt: 'Português',
  fr: 'Français',
  it: 'Italiano',
  tl: 'Filipino',
  'zh-TW': '繁體中文',
};

const en: T = {
  appSubtitle: 'AI-Powered Privacy Protection for Images & Videos',
  inputSelection: 'Input Selection',
  selectFilePlaceholder: 'Select a file or folder...',
  browseFile: 'Browse File',
  browseFolder: 'Browse Folder',
  folderFilter: 'Folder filter:',
  both: 'Both',
  imagesOnly: 'Images Only',
  videosOnly: 'Videos Only',
  processingMode: 'Processing Mode',
  blackMask: '⬛ Black Mask',
  blackMaskDesc: 'Recommended for maximum privacy',
  blurMode: '🌫️ Blur',
  blurModeDesc: 'Intelligent contour-following blur',
  blurSettings: 'Blur Settings (Blur Mode Only)',
  intensity: 'Intensity',
  passes: 'Passes:',
  morePassesStronger: 'More passes = stronger blur',
  advancedSettings: 'Advanced Settings',
  confidence: 'Confidence',
  personModel: 'Person Model',
  enableSkinDetection: 'Enable Skin Tone Detection',
  skinDetectionDesc: 'Detects skin tones near YOLO regions for better coverage',
  outputSettings: 'Output Settings',
  filenameSuffix: 'Filename Suffix',
  frameInterval: 'Frame Interval (videos)',
  frameIntervalDesc: '1 = every frame, 3 = every 3rd frame',
  keepAudio: '🔊 Keep audio in output videos',
  keepAudioDesc: 'Requires ffmpeg',
  audioDisabledDesc: 'Auto-disabled with frame skipping',
  processMedia: '🚀 Process Media',
  processingBtn: 'Processing...',
  cancel: 'Cancel',
  help: '❓ Help',
  settings: '⚙️ Settings',
  processingProgress: 'Processing Progress',
  individualFileProgress: 'Individual File Progress',
  overallProgress: 'Overall Progress (Batch)',
  ready: 'Ready to process media files',
  settingsTitle: 'Settings',
  language: 'Language',
  close: 'Close',
  guiUsage: 'GUI Usage',
  cliUsage: 'CLI Usage',
};

const es: T = {
  appSubtitle: 'Protección de privacidad con IA para imágenes y videos',
  inputSelection: 'Selección de entrada',
  selectFilePlaceholder: 'Selecciona un archivo o carpeta...',
  browseFile: 'Archivo',
  browseFolder: 'Carpeta',
  folderFilter: 'Filtro de carpeta:',
  both: 'Ambos',
  imagesOnly: 'Solo imágenes',
  videosOnly: 'Solo videos',
  processingMode: 'Modo de procesamiento',
  blackMask: '⬛ Máscara negra',
  blackMaskDesc: 'Recomendado para máxima privacidad',
  blurMode: '🌫️ Difuminado',
  blurModeDesc: 'Difuminado inteligente siguiendo contornos',
  blurSettings: 'Ajustes de difuminado (solo modo difuminado)',
  intensity: 'Intensidad',
  passes: 'Pasadas:',
  morePassesStronger: 'Más pasadas = difuminado más fuerte',
  advancedSettings: 'Ajustes avanzados',
  confidence: 'Confianza',
  personModel: 'Modelo de persona',
  enableSkinDetection: 'Activar detección de tono de piel',
  skinDetectionDesc: 'Detecta tonos de piel cerca de las regiones YOLO',
  outputSettings: 'Ajustes de salida',
  filenameSuffix: 'Sufijo del nombre de archivo',
  frameInterval: 'Intervalo de fotogramas (videos)',
  frameIntervalDesc: '1 = cada fotograma, 3 = cada 3er fotograma',
  keepAudio: '🔊 Conservar audio en videos de salida',
  keepAudioDesc: 'Requiere ffmpeg',
  audioDisabledDesc: 'Desactivado automáticamente con omisión de fotogramas',
  processMedia: '🚀 Procesar',
  processingBtn: 'Procesando...',
  cancel: 'Cancelar',
  help: '❓ Ayuda',
  settings: '⚙️ Ajustes',
  processingProgress: 'Progreso del procesamiento',
  individualFileProgress: 'Progreso del archivo',
  overallProgress: 'Progreso general (lote)',
  ready: 'Listo para procesar archivos multimedia',
  settingsTitle: 'Ajustes',
  language: 'Idioma',
  close: 'Cerrar',
  guiUsage: 'Uso de GUI',
  cliUsage: 'Uso de CLI',
};

const pt: T = {
  appSubtitle: 'Proteção de privacidade com IA para imagens e vídeos',
  inputSelection: 'Seleção de entrada',
  selectFilePlaceholder: 'Selecione um arquivo ou pasta...',
  browseFile: 'Arquivo',
  browseFolder: 'Pasta',
  folderFilter: 'Filtro de pasta:',
  both: 'Ambos',
  imagesOnly: 'Só imagens',
  videosOnly: 'Só vídeos',
  processingMode: 'Modo de processamento',
  blackMask: '⬛ Máscara preta',
  blackMaskDesc: 'Recomendado para máxima privacidade',
  blurMode: '🌫️ Desfoque',
  blurModeDesc: 'Desfoque inteligente seguindo contornos',
  blurSettings: 'Configurações de desfoque (somente modo desfoque)',
  intensity: 'Intensidade',
  passes: 'Passagens:',
  morePassesStronger: 'Mais passagens = desfoque mais forte',
  advancedSettings: 'Configurações avançadas',
  confidence: 'Confiança',
  personModel: 'Modelo de pessoa',
  enableSkinDetection: 'Ativar detecção de tom de pele',
  skinDetectionDesc: 'Detecta tons de pele próximos às regiões YOLO',
  outputSettings: 'Configurações de saída',
  filenameSuffix: 'Sufixo do nome do arquivo',
  frameInterval: 'Intervalo de quadros (vídeos)',
  frameIntervalDesc: '1 = cada quadro, 3 = a cada 3º quadro',
  keepAudio: '🔊 Manter áudio nos vídeos de saída',
  keepAudioDesc: 'Requer ffmpeg',
  audioDisabledDesc: 'Desativado automaticamente com salto de quadros',
  processMedia: '🚀 Processar',
  processingBtn: 'Processando...',
  cancel: 'Cancelar',
  help: '❓ Ajuda',
  settings: '⚙️ Configurações',
  processingProgress: 'Progresso do processamento',
  individualFileProgress: 'Progresso do arquivo',
  overallProgress: 'Progresso geral (lote)',
  ready: 'Pronto para processar arquivos de mídia',
  settingsTitle: 'Configurações',
  language: 'Idioma',
  close: 'Fechar',
  guiUsage: 'Uso da GUI',
  cliUsage: 'Uso da CLI',
};

const fr: T = {
  appSubtitle: "Protection de la vie privée par IA pour images et vidéos",
  inputSelection: 'Sélection des fichiers',
  selectFilePlaceholder: 'Sélectionnez un fichier ou un dossier...',
  browseFile: 'Fichier',
  browseFolder: 'Dossier',
  folderFilter: 'Filtre de dossier :',
  both: 'Les deux',
  imagesOnly: 'Images seulement',
  videosOnly: 'Vidéos seulement',
  processingMode: 'Mode de traitement',
  blackMask: '⬛ Masque noir',
  blackMaskDesc: 'Recommandé pour une confidentialité maximale',
  blurMode: '🌫️ Flou',
  blurModeDesc: 'Flou intelligent suivant les contours',
  blurSettings: 'Paramètres de flou (mode flou uniquement)',
  intensity: 'Intensité',
  passes: 'Passes :',
  morePassesStronger: 'Plus de passes = flou plus fort',
  advancedSettings: 'Paramètres avancés',
  confidence: 'Confiance',
  personModel: 'Modèle de personne',
  enableSkinDetection: 'Activer la détection de teinte de peau',
  skinDetectionDesc: 'Détecte les teintes de peau près des régions YOLO',
  outputSettings: 'Paramètres de sortie',
  filenameSuffix: 'Suffixe du nom de fichier',
  frameInterval: 'Intervalle de trames (vidéos)',
  frameIntervalDesc: '1 = chaque trame, 3 = chaque 3ème trame',
  keepAudio: '🔊 Conserver le son dans les vidéos de sortie',
  keepAudioDesc: 'Nécessite ffmpeg',
  audioDisabledDesc: 'Désactivé automatiquement avec le saut de trames',
  processMedia: '🚀 Traiter',
  processingBtn: 'Traitement...',
  cancel: 'Annuler',
  help: '❓ Aide',
  settings: '⚙️ Paramètres',
  processingProgress: 'Progression du traitement',
  individualFileProgress: 'Progression du fichier',
  overallProgress: 'Progression globale (lot)',
  ready: 'Prêt à traiter les fichiers multimédias',
  settingsTitle: 'Paramètres',
  language: 'Langue',
  close: 'Fermer',
  guiUsage: 'Utilisation GUI',
  cliUsage: 'Utilisation CLI',
};

const it: T = {
  appSubtitle: 'Protezione della privacy con IA per immagini e video',
  inputSelection: 'Selezione input',
  selectFilePlaceholder: 'Seleziona un file o una cartella...',
  browseFile: 'File',
  browseFolder: 'Cartella',
  folderFilter: 'Filtro cartella:',
  both: 'Entrambi',
  imagesOnly: 'Solo immagini',
  videosOnly: 'Solo video',
  processingMode: 'Modalità di elaborazione',
  blackMask: '⬛ Maschera nera',
  blackMaskDesc: 'Consigliato per la massima privacy',
  blurMode: '🌫️ Sfocatura',
  blurModeDesc: 'Sfocatura intelligente che segue i contorni',
  blurSettings: 'Impostazioni sfocatura (solo modalità sfocatura)',
  intensity: 'Intensità',
  passes: 'Passaggi:',
  morePassesStronger: 'Più passaggi = sfocatura più forte',
  advancedSettings: 'Impostazioni avanzate',
  confidence: 'Confidenza',
  personModel: 'Modello persona',
  enableSkinDetection: 'Abilita rilevamento tono della pelle',
  skinDetectionDesc: 'Rileva i toni della pelle vicino alle regioni YOLO',
  outputSettings: 'Impostazioni di output',
  filenameSuffix: 'Suffisso nome file',
  frameInterval: 'Intervallo fotogrammi (video)',
  frameIntervalDesc: '1 = ogni fotogramma, 3 = ogni 3° fotogramma',
  keepAudio: '🔊 Mantieni audio nei video di output',
  keepAudioDesc: 'Richiede ffmpeg',
  audioDisabledDesc: 'Disabilitato automaticamente con il salto di fotogrammi',
  processMedia: '🚀 Elabora',
  processingBtn: 'Elaborazione...',
  cancel: 'Annulla',
  help: '❓ Aiuto',
  settings: '⚙️ Impostazioni',
  processingProgress: 'Avanzamento elaborazione',
  individualFileProgress: 'Avanzamento file',
  overallProgress: 'Avanzamento globale (batch)',
  ready: 'Pronto per elaborare i file multimediali',
  settingsTitle: 'Impostazioni',
  language: 'Lingua',
  close: 'Chiudi',
  guiUsage: 'Uso GUI',
  cliUsage: 'Uso CLI',
};

const tl: T = {
  appSubtitle: 'AI na Proteksyon ng Privacy para sa Mga Larawan at Video',
  inputSelection: 'Pagpili ng Input',
  selectFilePlaceholder: 'Pumili ng file o folder...',
  browseFile: 'File',
  browseFolder: 'Folder',
  folderFilter: 'Filter ng folder:',
  both: 'Pareho',
  imagesOnly: 'Mga larawan lamang',
  videosOnly: 'Mga video lamang',
  processingMode: 'Mode ng Pagproseso',
  blackMask: '⬛ Itim na Maskara',
  blackMaskDesc: 'Inirerekomenda para sa pinakamataas na privacy',
  blurMode: '🌫️ Blur',
  blurModeDesc: 'Matalinong blur na sumusunod sa balangkas',
  blurSettings: 'Mga Setting ng Blur (Blur Mode Lamang)',
  intensity: 'Lakas',
  passes: 'Mga Pagdaraan:',
  morePassesStronger: 'Mas maraming pagdaraan = mas malakas na blur',
  advancedSettings: 'Mga Advanced na Setting',
  confidence: 'Kumpiyansa',
  personModel: 'Modelo ng Tao',
  enableSkinDetection: 'I-aktibo ang Pagtuklas ng Kulay ng Balat',
  skinDetectionDesc: 'Nakakakita ng mga kulay ng balat malapit sa mga rehiyon ng YOLO',
  outputSettings: 'Mga Setting ng Output',
  filenameSuffix: 'Suffix ng Pangalan ng File',
  frameInterval: 'Agwat ng Frame (mga video)',
  frameIntervalDesc: '1 = bawat frame, 3 = bawat ika-3 na frame',
  keepAudio: '🔊 Panatilihin ang audio sa output na mga video',
  keepAudioDesc: 'Nangangailangan ng ffmpeg',
  audioDisabledDesc: 'Awtomatikong hindi pinagana sa frame skipping',
  processMedia: '🚀 Proseso',
  processingBtn: 'Pinoproseso...',
  cancel: 'Kanselahin',
  help: '❓ Tulong',
  settings: '⚙️ Mga Setting',
  processingProgress: 'Progreso ng Pagproseso',
  individualFileProgress: 'Progreso ng File',
  overallProgress: 'Pangkalahatang Progreso (Batch)',
  ready: 'Handa nang magproseso ng mga media file',
  settingsTitle: 'Mga Setting',
  language: 'Wika',
  close: 'Isara',
  guiUsage: 'Paggamit ng GUI',
  cliUsage: 'Paggamit ng CLI',
};

const zhTW: T = {
  appSubtitle: 'AI 驅動的圖片與影片隱私保護工具',
  inputSelection: '選擇輸入',
  selectFilePlaceholder: '選擇檔案或資料夾...',
  browseFile: '選擇檔案',
  browseFolder: '選擇資料夾',
  folderFilter: '資料夾篩選：',
  both: '全部',
  imagesOnly: '僅圖片',
  videosOnly: '僅影片',
  processingMode: '處理模式',
  blackMask: '⬛ 黑色遮罩',
  blackMaskDesc: '推薦使用，提供最大隱私保護',
  blurMode: '🌫️ 模糊',
  blurModeDesc: '智能輪廓追蹤模糊',
  blurSettings: '模糊設定（僅限模糊模式）',
  intensity: '強度',
  passes: '次數：',
  morePassesStronger: '次數越多 = 模糊效果越強',
  advancedSettings: '進階設定',
  confidence: '信心度',
  personModel: '人物模型',
  enableSkinDetection: '啟用膚色偵測',
  skinDetectionDesc: '偵測 YOLO 區域附近的膚色以提高覆蓋率',
  outputSettings: '輸出設定',
  filenameSuffix: '檔案名稱後綴',
  frameInterval: '幀間隔（影片）',
  frameIntervalDesc: '1 = 每幀，3 = 每第 3 幀',
  keepAudio: '🔊 保留輸出影片中的音訊',
  keepAudioDesc: '需要 ffmpeg',
  audioDisabledDesc: '使用跳幀時自動停用',
  processMedia: '🚀 開始處理',
  processingBtn: '處理中...',
  cancel: '取消',
  help: '❓ 說明',
  settings: '⚙️ 設定',
  processingProgress: '處理進度',
  individualFileProgress: '單一檔案進度',
  overallProgress: '整體進度（批次）',
  ready: '準備好處理媒體檔案',
  settingsTitle: '設定',
  language: '語言',
  close: '關閉',
  guiUsage: 'GUI 使用說明',
  cliUsage: 'CLI 使用說明',
};

export const translations: Record<Language, T> = {
  en,
  es,
  pt,
  fr,
  it,
  tl,
  'zh-TW': zhTW,
};
