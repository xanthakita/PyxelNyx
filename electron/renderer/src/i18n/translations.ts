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
  officerName: string;
  officerNamePlaceholder: string;
  officerNameHelper: string;
  caseNumber: string;
  caseNumberPlaceholder: string;
  caseNumberHelper: string;
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

  // Help Dialog content
  guiHelp: string;
  cliHelp: string;
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
  officerName: 'Officer Name',
  officerNamePlaceholder: 'e.g. J. Smith',
  officerNameHelper: 'Added to output filename',
  caseNumber: 'Case Number',
  caseNumberPlaceholder: 'e.g. 2024-001',
  caseNumberHelper: 'Added to output filename',
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
  guiHelp: `OVERVIEW
PyxelNyx automatically detects and masks/blurs humans in images and videos using AI (YOLOv8 segmentation).

GETTING STARTED
1. Select Input: Click "Browse File" for a single file, or "Browse Folder" for batch processing
2. Choose Mask Type: Black Mask (default) or Blur
3. Adjust Settings (Optional): blur intensity, passes, confidence, model, skin tone detection
4. Configure Output Settings (Optional): filename suffix, frame interval, audio handling
5. Click "Process Media"

SUPPORTED FORMATS
Images: .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Videos: .mp4 .mov

OUTPUT
Processed files are saved with your chosen suffix (default "-background"):
  photo.jpg → photo-background.jpg
  video.mp4 → video-background.mp4
Original files are never modified.

TIPS
• For speed: Use default yolov8n-seg.pt model
• For accuracy: Use yolov8m-seg.pt or higher
• Lower confidence (0.3): Detect more people (more false positives)
• Higher confidence (0.7): Stricter detection (fewer false positives)
• Black mask mode is fastest

ERRORS
If you encounter unsupported file errors: apps@globalemancipation.ngo`,
  cliHelp: `BASIC USAGE
Process a single image with black mask (default):
  python blur_humans.py photo.jpg

Process with blur instead of black mask:
  python blur_humans.py photo.jpg --mask-type blur

Process a video:
  python blur_humans.py video.mp4

Process all files in a directory:
  python blur_humans.py /path/to/media/

ADVANCED OPTIONS
Extreme blur with more passes:
  python blur_humans.py photo.jpg --mask-type blur --blur 201 --passes 5

Adjust detection sensitivity:
  python blur_humans.py photo.jpg --confidence 0.7

Use more accurate model (slower):
  python blur_humans.py photo.jpg --model yolov8m-seg.pt

COMMAND-LINE ARGUMENTS
input               Path to image/video file or directory (required)
--media-type        Media filter: images, videos, both (default: both)
--mask-type, -t     Masking type: black or blur (default: black)
--blur, -b          Blur kernel size 1-301 (default: 151)
--passes, -p        Number of blur passes 1-10 (default: 3)
--confidence, -c    Detection threshold 0.0-1.0 (default: 0.33)
--model, -m         YOLO model selection (default: yolov8n-seg.pt)

MODEL SELECTION
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Default, fastest
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Good balance
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Higher accuracy
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Professional use
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Maximum accuracy`,
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
  officerName: 'Nombre del oficial',
  officerNamePlaceholder: 'p.ej. J. García',
  officerNameHelper: 'Se añade al nombre del archivo de salida',
  caseNumber: 'Número de caso',
  caseNumberPlaceholder: 'p.ej. 2024-001',
  caseNumberHelper: 'Se añade al nombre del archivo de salida',
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
  guiHelp: `DESCRIPCIÓN GENERAL
PyxelNyx detecta y enmascara/difumina automáticamente a las personas en imágenes y videos usando IA (segmentación YOLOv8).

PRIMEROS PASOS
1. Seleccionar entrada: Haz clic en "Archivo" para un solo archivo, o "Carpeta" para procesamiento por lotes
2. Elegir tipo de máscara: Máscara negra (predeterminado) o Difuminado
3. Ajustar configuración (opcional): intensidad de difuminado, pasadas, confianza, modelo, detección de tono de piel
4. Configurar ajustes de salida (opcional): sufijo de nombre de archivo, intervalo de fotogramas, manejo de audio
5. Hacer clic en "Procesar"

FORMATOS COMPATIBLES
Imágenes: .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Videos: .mp4 .mov

SALIDA
Los archivos procesados se guardan con el sufijo elegido (predeterminado "-background"):
  foto.jpg → foto-background.jpg
  video.mp4 → video-background.mp4
Los archivos originales nunca se modifican.

CONSEJOS
• Para velocidad: Usa el modelo predeterminado yolov8n-seg.pt
• Para precisión: Usa yolov8m-seg.pt o superior
• Confianza baja (0.3): Detecta más personas (más falsos positivos)
• Confianza alta (0.7): Detección más estricta (menos falsos positivos)
• El modo máscara negra es el más rápido

ERRORES
Si encuentras errores de archivos no compatibles: apps@globalemancipation.ngo`,
  cliHelp: `USO BÁSICO
Procesar una imagen con máscara negra (predeterminado):
  python blur_humans.py foto.jpg

Procesar con difuminado en lugar de máscara negra:
  python blur_humans.py foto.jpg --mask-type blur

Procesar un video:
  python blur_humans.py video.mp4

Procesar todos los archivos en un directorio:
  python blur_humans.py /ruta/a/medios/

OPCIONES AVANZADAS
Difuminado extremo con más pasadas:
  python blur_humans.py foto.jpg --mask-type blur --blur 201 --passes 5

Ajustar sensibilidad de detección:
  python blur_humans.py foto.jpg --confidence 0.7

Usar modelo más preciso (más lento):
  python blur_humans.py foto.jpg --model yolov8m-seg.pt

ARGUMENTOS DE LÍNEA DE COMANDOS
input               Ruta al archivo/video o directorio (requerido)
--media-type        Filtro: images, videos, both (predeterminado: both)
--mask-type, -t     Tipo de máscara: black o blur (predeterminado: black)
--blur, -b          Tamaño del núcleo de difuminado 1-301 (predeterminado: 151)
--passes, -p        Número de pasadas de difuminado 1-10 (predeterminado: 3)
--confidence, -c    Umbral de detección 0.0-1.0 (predeterminado: 0.33)
--model, -m         Selección del modelo YOLO (predeterminado: yolov8n-seg.pt)

SELECCIÓN DE MODELO
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Predeterminado, más rápido
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Buen equilibrio
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Mayor precisión
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Uso profesional
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Máxima precisión`,
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
  officerName: 'Nome do oficial',
  officerNamePlaceholder: 'ex: J. Silva',
  officerNameHelper: 'Adicionado ao nome do arquivo de saída',
  caseNumber: 'Número do caso',
  caseNumberPlaceholder: 'ex: 2024-001',
  caseNumberHelper: 'Adicionado ao nome do arquivo de saída',
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
  guiHelp: `VISÃO GERAL
PyxelNyx detecta e mascara/desfoca automaticamente pessoas em imagens e vídeos usando IA (segmentação YOLOv8).

PRIMEIROS PASSOS
1. Selecionar entrada: Clique em "Arquivo" para um único arquivo, ou "Pasta" para processamento em lote
2. Escolher tipo de máscara: Máscara preta (padrão) ou Desfoque
3. Ajustar configurações (opcional): intensidade do desfoque, passagens, confiança, modelo, detecção de tom de pele
4. Configurar ajustes de saída (opcional): sufixo do nome do arquivo, intervalo de quadros, áudio
5. Clicar em "Processar"

FORMATOS SUPORTADOS
Imagens: .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Vídeos: .mp4 .mov

SAÍDA
Os arquivos processados são salvos com o sufixo escolhido (padrão "-background"):
  foto.jpg → foto-background.jpg
  video.mp4 → video-background.mp4
Os arquivos originais nunca são modificados.

DICAS
• Para velocidade: Use o modelo padrão yolov8n-seg.pt
• Para precisão: Use yolov8m-seg.pt ou superior
• Confiança baixa (0.3): Detecta mais pessoas (mais falsos positivos)
• Confiança alta (0.7): Detecção mais rigorosa (menos falsos positivos)
• O modo máscara preta é o mais rápido

ERROS
Se encontrar erros de arquivos não suportados: apps@globalemancipation.ngo`,
  cliHelp: `USO BÁSICO
Processar uma imagem com máscara preta (padrão):
  python blur_humans.py foto.jpg

Processar com desfoque em vez de máscara preta:
  python blur_humans.py foto.jpg --mask-type blur

Processar um vídeo:
  python blur_humans.py video.mp4

Processar todos os arquivos em um diretório:
  python blur_humans.py /caminho/para/mídia/

OPÇÕES AVANÇADAS
Desfoque extremo com mais passagens:
  python blur_humans.py foto.jpg --mask-type blur --blur 201 --passes 5

Ajustar sensibilidade de detecção:
  python blur_humans.py foto.jpg --confidence 0.7

Usar modelo mais preciso (mais lento):
  python blur_humans.py foto.jpg --model yolov8m-seg.pt

ARGUMENTOS DE LINHA DE COMANDO
input               Caminho para arquivo/vídeo ou diretório (obrigatório)
--media-type        Filtro: images, videos, both (padrão: both)
--mask-type, -t     Tipo de máscara: black ou blur (padrão: black)
--blur, -b          Tamanho do kernel de desfoque 1-301 (padrão: 151)
--passes, -p        Número de passagens de desfoque 1-10 (padrão: 3)
--confidence, -c    Limite de detecção 0.0-1.0 (padrão: 0.33)
--model, -m         Seleção do modelo YOLO (padrão: yolov8n-seg.pt)

SELEÇÃO DE MODELO
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Padrão, mais rápido
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Bom equilíbrio
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Maior precisão
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Uso profissional
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Precisão máxima`,
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
  officerName: "Nom de l'officier",
  officerNamePlaceholder: 'ex. : J. Dupont',
  officerNameHelper: 'Ajouté au nom du fichier de sortie',
  caseNumber: 'Numéro de dossier',
  caseNumberPlaceholder: 'ex. : 2024-001',
  caseNumberHelper: 'Ajouté au nom du fichier de sortie',
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
  guiHelp: `APERÇU
PyxelNyx détecte et masque/floute automatiquement les personnes dans les images et vidéos grâce à l'IA (segmentation YOLOv8).

DÉMARRAGE
1. Sélectionner l'entrée : Cliquez sur « Fichier » pour un seul fichier, ou « Dossier » pour le traitement par lot
2. Choisir le type de masque : Masque noir (par défaut) ou Flou
3. Ajuster les paramètres (optionnel) : intensité du flou, passes, confiance, modèle, détection du teint
4. Configurer les paramètres de sortie (optionnel) : suffixe du nom de fichier, intervalle de trames, audio
5. Cliquer sur « Traiter »

FORMATS PRIS EN CHARGE
Images : .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Vidéos : .mp4 .mov

RÉSULTATS
Les fichiers traités sont enregistrés avec le suffixe choisi (par défaut "-background") :
  photo.jpg → photo-background.jpg
  video.mp4 → video-background.mp4
Les fichiers originaux ne sont jamais modifiés.

CONSEILS
• Pour la vitesse : Utilisez le modèle par défaut yolov8n-seg.pt
• Pour la précision : Utilisez yolov8m-seg.pt ou supérieur
• Confiance basse (0.3) : Détecte plus de personnes (plus de faux positifs)
• Confiance haute (0.7) : Détection plus stricte (moins de faux positifs)
• Le mode masque noir est le plus rapide

ERREURS
Si vous rencontrez des erreurs de fichiers non pris en charge : apps@globalemancipation.ngo`,
  cliHelp: `UTILISATION DE BASE
Traiter une image avec masque noir (par défaut) :
  python blur_humans.py photo.jpg

Traiter avec flou au lieu du masque noir :
  python blur_humans.py photo.jpg --mask-type blur

Traiter une vidéo :
  python blur_humans.py video.mp4

Traiter tous les fichiers d'un répertoire :
  python blur_humans.py /chemin/vers/médias/

OPTIONS AVANCÉES
Flou extrême avec plus de passes :
  python blur_humans.py photo.jpg --mask-type blur --blur 201 --passes 5

Ajuster la sensibilité de détection :
  python blur_humans.py photo.jpg --confidence 0.7

Utiliser un modèle plus précis (plus lent) :
  python blur_humans.py photo.jpg --model yolov8m-seg.pt

ARGUMENTS EN LIGNE DE COMMANDE
input               Chemin vers le fichier/vidéo ou répertoire (requis)
--media-type        Filtre : images, videos, both (par défaut : both)
--mask-type, -t     Type de masque : black ou blur (par défaut : black)
--blur, -b          Taille du noyau de flou 1-301 (par défaut : 151)
--passes, -p        Nombre de passes de flou 1-10 (par défaut : 3)
--confidence, -c    Seuil de détection 0.0-1.0 (par défaut : 0.33)
--model, -m         Sélection du modèle YOLO (par défaut : yolov8n-seg.pt)

SÉLECTION DU MODÈLE
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Par défaut, le plus rapide
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Bon équilibre
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Meilleure précision
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Usage professionnel
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Précision maximale`,
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
  officerName: "Nome dell'ufficiale",
  officerNamePlaceholder: 'es. G. Rossi',
  officerNameHelper: 'Aggiunto al nome del file di output',
  caseNumber: 'Numero caso',
  caseNumberPlaceholder: 'es. 2024-001',
  caseNumberHelper: 'Aggiunto al nome del file di output',
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
  guiHelp: `PANORAMICA
PyxelNyx rileva e maschera/sfoca automaticamente le persone in immagini e video usando l'IA (segmentazione YOLOv8).

INIZIARE
1. Seleziona input: Clicca su "File" per un singolo file, o "Cartella" per elaborazione batch
2. Scegli tipo di maschera: Maschera nera (predefinito) o Sfocatura
3. Regola le impostazioni (opzionale): intensità sfocatura, passaggi, confidenza, modello, rilevamento tono pelle
4. Configura impostazioni output (opzionale): suffisso nome file, intervallo fotogrammi, audio
5. Clicca su "Elabora"

FORMATI SUPPORTATI
Immagini: .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Video: .mp4 .mov

OUTPUT
I file elaborati vengono salvati con il suffisso scelto (predefinito "-background"):
  foto.jpg → foto-background.jpg
  video.mp4 → video-background.mp4
I file originali non vengono mai modificati.

SUGGERIMENTI
• Per la velocità: Usa il modello predefinito yolov8n-seg.pt
• Per la precisione: Usa yolov8m-seg.pt o superiore
• Confidenza bassa (0.3): Rileva più persone (più falsi positivi)
• Confidenza alta (0.7): Rilevamento più rigoroso (meno falsi positivi)
• La modalità maschera nera è la più veloce

ERRORI
Se riscontri errori con file non supportati: apps@globalemancipation.ngo`,
  cliHelp: `UTILIZZO DI BASE
Elaborare un'immagine con maschera nera (predefinito):
  python blur_humans.py foto.jpg

Elaborare con sfocatura invece della maschera nera:
  python blur_humans.py foto.jpg --mask-type blur

Elaborare un video:
  python blur_humans.py video.mp4

Elaborare tutti i file in una directory:
  python blur_humans.py /percorso/ai/media/

OPZIONI AVANZATE
Sfocatura estrema con più passaggi:
  python blur_humans.py foto.jpg --mask-type blur --blur 201 --passes 5

Regolare la sensibilità di rilevamento:
  python blur_humans.py foto.jpg --confidence 0.7

Usare un modello più preciso (più lento):
  python blur_humans.py foto.jpg --model yolov8m-seg.pt

ARGOMENTI DA RIGA DI COMANDO
input               Percorso al file/video o directory (obbligatorio)
--media-type        Filtro: images, videos, both (predefinito: both)
--mask-type, -t     Tipo di maschera: black o blur (predefinito: black)
--blur, -b          Dimensione kernel sfocatura 1-301 (predefinito: 151)
--passes, -p        Numero di passaggi di sfocatura 1-10 (predefinito: 3)
--confidence, -c    Soglia di rilevamento 0.0-1.0 (predefinito: 0.33)
--model, -m         Selezione modello YOLO (predefinito: yolov8n-seg.pt)

SELEZIONE MODELLO
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Predefinito, più veloce
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Buon equilibrio
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Maggiore precisione
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Uso professionale
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Precisione massima`,
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
  officerName: 'Pangalan ng Opisyal',
  officerNamePlaceholder: 'hal. J. Santos',
  officerNameHelper: 'Idadagdag sa pangalan ng output file',
  caseNumber: 'Numero ng Kaso',
  caseNumberPlaceholder: 'hal. 2024-001',
  caseNumberHelper: 'Idadagdag sa pangalan ng output file',
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
  guiHelp: `PANGKALAHATANG-IDEYA
Awtomatikong nakita at nino-mask/bina-blur ng PyxelNyx ang mga tao sa mga larawan at video gamit ang AI (YOLOv8 segmentation).

PAGSISIMULA
1. Piliin ang input: I-click ang "File" para sa isang file, o "Folder" para sa batch processing
2. Piliin ang uri ng mask: Itim na maskara (default) o Blur
3. Ayusin ang mga setting (opsyonal): lakas ng blur, mga pagdaraan, kumpiyansa, modelo, pagtuklas ng kulay ng balat
4. I-configure ang mga setting ng output (opsyonal): suffix ng pangalan ng file, agwat ng frame, audio
5. I-click ang "Proseso"

MGA SINUSUPORTAHANG FORMAT
Mga larawan: .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Mga video: .mp4 .mov

OUTPUT
Ang mga naprosesong file ay nai-save na may piniling suffix (default "-background"):
  larawan.jpg → larawan-background.jpg
  video.mp4 → video-background.mp4
Ang mga orihinal na file ay hindi kailanman binabago.

MGA TIPS
• Para sa bilis: Gamitin ang default na model na yolov8n-seg.pt
• Para sa katumpakan: Gamitin ang yolov8m-seg.pt o mas mataas
• Mababang kumpiyansa (0.3): Nakakakita ng mas maraming tao (mas maraming maling positibo)
• Mataas na kumpiyansa (0.7): Mas mahigpit na pagtuklas (mas kaunting maling positibo)
• Ang itim na maskara ay pinakamabilis

MGA ERROR
Kung makaranas ng mga error sa hindi sinusuportahang file: apps@globalemancipation.ngo`,
  cliHelp: `PANGUNAHING PAGGAMIT
Mag-proseso ng isang larawan gamit ang itim na maskara (default):
  python blur_humans.py larawan.jpg

Mag-proseso gamit ang blur sa halip na itim na maskara:
  python blur_humans.py larawan.jpg --mask-type blur

Mag-proseso ng video:
  python blur_humans.py video.mp4

Mag-proseso ng lahat ng file sa isang direktoryo:
  python blur_humans.py /landas/sa/media/

MGA ADVANCED NA OPSYON
Matinding blur na may mas maraming pagdaraan:
  python blur_humans.py larawan.jpg --mask-type blur --blur 201 --passes 5

Ayusin ang sensitivity ng pagtuklas:
  python blur_humans.py larawan.jpg --confidence 0.7

Gumamit ng mas tumpak na modelo (mas mabagal):
  python blur_humans.py larawan.jpg --model yolov8m-seg.pt

MGA ARGUMENTO SA COMMAND LINE
input               Landas sa file/video o direktoryo (kinakailangan)
--media-type        Filter: images, videos, both (default: both)
--mask-type, -t     Uri ng maskara: black o blur (default: black)
--blur, -b          Laki ng blur kernel 1-301 (default: 151)
--passes, -p        Bilang ng mga pagdaraan ng blur 1-10 (default: 3)
--confidence, -c    Threshold ng pagtuklas 0.0-1.0 (default: 0.33)
--model, -m         Pagpili ng YOLO model (default: yolov8n-seg.pt)

PAGPILI NG MODELO
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Default, pinakamabilis
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Magandang balanse
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Mas mataas na katumpakan
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Propesyonal na paggamit
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Pinakamataas na katumpakan`,
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
  officerName: '官員姓名',
  officerNamePlaceholder: '例如：王小明',
  officerNameHelper: '將附加至輸出檔案名稱',
  caseNumber: '案件編號',
  caseNumberPlaceholder: '例如：2024-001',
  caseNumberHelper: '將附加至輸出檔案名稱',
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
  guiHelp: `概覽
PyxelNyx 使用 AI（YOLOv8 分割技術）自動偵測並遮蔽／模糊圖片和影片中的人物。

快速開始
1. 選擇輸入：點擊「選擇檔案」處理單一檔案，或「選擇資料夾」進行批次處理
2. 選擇遮蔽類型：黑色遮罩（預設）或模糊
3. 調整設定（選填）：模糊強度、次數、信心度、模型、膚色偵測
4. 設定輸出選項（選填）：檔案名稱後綴、幀間隔、音訊處理
5. 點擊「開始處理」

支援的格式
圖片：.jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
影片：.mp4 .mov

輸出
處理後的檔案以所選後綴儲存（預設為「-background」）：
  照片.jpg → 照片-background.jpg
  影片.mp4 → 影片-background.mp4
原始檔案永遠不會被修改。

使用技巧
• 追求速度：使用預設的 yolov8n-seg.pt 模型
• 追求精準：使用 yolov8m-seg.pt 或更高
• 低信心度（0.3）：偵測更多人物（較多誤判）
• 高信心度（0.7）：更嚴格的偵測（較少誤判）
• 黑色遮罩模式速度最快

錯誤
如果遇到不支援的檔案錯誤，請聯絡：apps@globalemancipation.ngo`,
  cliHelp: `基本用法
使用黑色遮罩處理單張圖片（預設）：
  python blur_humans.py 照片.jpg

使用模糊代替黑色遮罩：
  python blur_humans.py 照片.jpg --mask-type blur

處理影片：
  python blur_humans.py 影片.mp4

處理目錄中的所有檔案：
  python blur_humans.py /媒體/路徑/

進階選項
使用更多次數進行強力模糊：
  python blur_humans.py 照片.jpg --mask-type blur --blur 201 --passes 5

調整偵測靈敏度：
  python blur_humans.py 照片.jpg --confidence 0.7

使用更精準的模型（較慢）：
  python blur_humans.py 照片.jpg --model yolov8m-seg.pt

命令列參數
input               圖片/影片檔案或目錄路徑（必填）
--media-type        媒體篩選：images、videos、both（預設：both）
--mask-type, -t     遮蔽類型：black 或 blur（預設：black）
--blur, -b          模糊核心大小 1-301（預設：151）
--passes, -p        模糊次數 1-10（預設：3）
--confidence, -c    偵測閾值 0.0-1.0（預設：0.33）
--model, -m         YOLO 模型選擇（預設：yolov8n-seg.pt）

模型選擇
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       預設，最快
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     良好平衡
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   更高精準度
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   專業用途
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   最高精準度`,
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
