#  Face Detection com Câmera IP ONVIF

Este projeto é uma aplicação simples em Python que utiliza uma câmera IP com protocolo ONVIF para detectar rostos e contar quantas pessoas foram identificadas na frente da câmera. Ele usa a biblioteca `OpenCV` para captura de vídeo e detecção de rostos, e `face_recognition` para o reconhecimento e contagem de rostos.

Além disso, o projeto registra a data e a hora de cada rosto identificado em um arquivo de texto, mantendo um identificador único para cada rosto.

## Pré-requisitos

- Python 3.8
- Miniconda
- CMake
- Visual Studio Build Tools

## Instalação Windows 

1. **Instalar Python**:
   - Baixe e instale o Python em [python.org](https://www.python.org/downloads/).

2. **Instalar Miniconda**:
   - Baixe e instale o Miniconda em [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

3. **Criar e Ativar um Ambiente Conda**:
   - Abra o "Anaconda Prompt" e execute:
     ```bash
     conda create -n face_recognition_env python=3.8
     conda activate face_recognition_env
     ```

4. **Instalar CMake**:
   - Baixe e instale o CMake em [cmake.org](https://cmake.org/download/).
   - Adicione o CMake ao PATH durante a instalação.

5. **Instalar Visual Studio Build Tools**:
   - Baixe e instale o Visual Studio Build Tools em [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   - Selecione "Desktop development with C++" durante a instalação.

6. **Instalar Dependências**:
   ```bash
   conda install -c conda-forge dlib
   pip install opencv-python-headless face_recognition onvif-zeep


## Instalação Linux

1. **Instalar Python**:
   - Baixe e instale o Python em [python.org](https://www.python.org/downloads/).

2. **Instalar Miniconda**:
   - Baixe e instale o Miniconda em [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

3. **Criar e Ativar um Ambiente Conda**:
   - Abra o "Anaconda Prompt" e execute:
     ```bash
     conda create -n face_recognition_env python=3.8
     conda activate face_recognition_env
     ```

4. **Instalar CMake**:
   - Baixe e instale o CMake em [cmake.org](https://cmake.org/download/).
   - Adicione o CMake ao PATH durante a instalação.

5. **Instalar Visual Studio Build Tools**:
   - Baixe e instale o Visual Studio Build Tools em [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   - Selecione "Desktop development with C++" durante a instalação.

6. **Instalar Dependências**:
   ```bash
   conda install -c conda-forge dlib
   pip install opencv-python-headless face_recognition onvif-zeep
