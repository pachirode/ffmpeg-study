# Log options
DEBUG = True

# GRPC options
MAX_MESSAGE_LENGTH = 100 * 1024 * 1024
grpc_options = [
    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
]
