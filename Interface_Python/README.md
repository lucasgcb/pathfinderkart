# Interface Python

- Utiliza Pyside 2
- Utiliza Multithreading
- Utiliza PySerial
---

Arquivo principal: janela_medidor.py

Definições de maquina de estado: 
- corretor_cpt_defs.py
- corretor_pathfind_defs.py

Threads:
- scanner.py
    - Envia e recebe informações para o microcontrolador. 
    - Grava nível de bateria e passa informações para queue.
- vigia_sensor.py
    - Verifica informação de sensor recebida, converte em lista. Armazena em queue.
    - Apenas armazena na queue se o valor for diferente do anterior.
- corretor_pathfind.py
    - Lê informação de sensor enviado pelo vigia.
    - Envia informação para máquina de estados.
    - Ativa máquina de estados. A máquina de estados envia comando para um espaço global, legível pelo scanner.

