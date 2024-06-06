from azure.servicebus import ServiceBusClient
from azure.servicebus import ServiceBusMessage


def send_message(CONNECTION_STR, QUEUE_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
    message = ServiceBusMessage("Temperatura maxima interna excedida")
    sender.send_messages(message)

    sender.close()
    servicebus_client.close()

    return "sucess"


def receiver_message(CONNECTION_STR, QUEUE_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
    retorno = None

    with receiver:
        for message in receiver:
            retorno = message
            print(message)
            receiver.complete_message(message)
            break

    servicebus_client.close()

    return retorno


if __name__ == '__main__':
    resultado = send_message(CONNECTION_STR, QUEUE_NAME)
    print(resultado)

    print(receiver_message(CONNECTION_STR, QUEUE_NAME))
