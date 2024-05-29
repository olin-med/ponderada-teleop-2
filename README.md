# Teleoperação do TurtleBot3 com Interface Web

Este projeto fornece uma interface web para teleoperar um robô TurtleBot3. A interface inclui botões para controlar o movimento do robô, exibe o feed da webcam com informações de latência, mostra as velocidades linear e angular do robô em tempo real, e inclui um botão para matar o nó de teleoperação.

## Pré-requisitos

- ROS2 (Humble ou posterior)
- Pacotes TurtleBot3
- Python3
- Flask
- OpenCV
- Flask-CORS

## Instruções de Configuração

### Instalar ROS2 e Pacotes TurtleBot3

Siga os guias oficiais de instalação do ROS2 e TurtleBot3 para configurar seu ambiente.

### Criar um Workspace ROS2

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### Clonar o Repositório do Projeto

```bash
cd ~/ros2_ws/src
git clone https://github.com/olin-med/ponderada-teleop-2
```

### Instalar Dependências Python

Certifique-se de ter `pip` instalado e então execute:

```bash
pip install flask flask-cors opencv-python
```

### Construir o Workspace

```bash
cd ~/ros2_ws
colcon build --packages-select turtlebot3_teleop_web
source install/setup.bash
```

## Executando o Nó de Teleoperação

```bash
ros2 run teleop_turtlebot teleop_node
```

## Acessando a Interface Web

Abra o arquivo `index.html` no seu navegador web. Você pode fazer isso simplesmente clicando duas vezes no arquivo ou abrindo-o através do diálogo "Open File" do seu navegador.

## Funcionalidades da Interface Web

- **Controle de Movimento**: Use os botões de seta para controlar o movimento do robô.
- **Feed da Webcam**: O feed da webcam do robô é exibido com informações de latência sobrepostas.
- **Exibição de Velocidade**: As velocidades linear e angular atuais do robô são exibidas em tempo real.
- **Botão de Desligamento**: Um botão para desligar o nó de teleoperação.

## Detalhes dos Scripts

### `teleop_node.py`

Este script inicializa um nó ROS2, lida com comandos de movimento da interface web, publica comandos de velocidade, transmite o feed da webcam e calcula a latência.

### `index.html`

Este arquivo HTML fornece a interface web para teleoperar o TurtleBot3. Inclui botões para controle de movimento, exibe o feed da webcam, mostra informações de velocidade e inclui um botão de desligamento.

## Solução de Problemas

1. **Erros de Inicialização do Nó**: Certifique-se de que o ROS2 está corretamente "sourced" e que todas as dependências estão instaladas.
2. **Problemas com o Feed da Webcam**: Verifique se sua webcam está conectada e acessível pelo OpenCV.
3. **Erros de CORS**: Certifique-se de que o Flask-CORS está instalado e corretamente configurado no script `teleop_node.py`.

