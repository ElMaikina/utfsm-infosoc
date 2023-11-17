from client import connect_to_server, send_data, verify_email_rut, disconnect_from_server


def main():
    connect_to_server()

    #cosas juas juas
    
    print(verify_email_rut("ayudasaaa@xdxd.cl", "88888-8"))
    print(send_data("88888-8", "ayudaaaa@xdxd.cl", 60,30,100))
    disconnect_from_server()


if __name__ == "__main__":
    main()