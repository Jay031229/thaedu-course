1. During the ELK Demo:
    - Launch the kibana : https://lvmql700:5601/
        - If not able to login.
            - Open Insomania : 
            - Check the biggest indeces. 
            - Perform the delete indeces.
            - Retry to login.
        - Username : elastic
        - Password: 
            kubectl get secret my-elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode
            JN4d20osHq5R96q79dGg5qs2
    - In this Demo going to present the logs directly from the HAC and NRL systems. 
    - Filebeat should be up and running on all systems. 
        - Filebeat check :
            
