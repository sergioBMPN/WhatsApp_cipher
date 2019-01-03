# from selenium import webdriver
#
# driver = webdriver.Firefox(executable_path = '/home/sergiobmpn/PycharmProjects/prueba1/geckodriver-v0.23.0-linux64/geckodriver')
# driver.get('http://web.whatsapp.com')
#
# name = input('Enter the name of user or group : ')
# msg = input('Enter the message : ')
# count = int(input('Enter the count : '))
#
# #Scan the code before proceeding further
# input('Enter anything after scanning QR code')
#
# user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
# user.click()
#
# msg_box = driver.find_element_by_class_name('input-container')
#
# for i in range(count):
#     msg_box.send_keys(msg)
# driver.find_element_by_class_name('compose-btn-send').click()

from selenium import webdriver

driver = webdriver.Firefox(executable_path = './geckodriver-v0.23.0-linux64/geckodriver')
driver.get('https://web.whatsapp.com/')


def send_msg():

    name = input('Introduce el nombre de usuario o grupo : ')
    try:
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
        user.click()

        msg_box = driver.find_element_by_class_name('_2S1VP')
    except:
        print("Error de version:actualiza el repositorio")

    msg = input('Escribe el mensaje: ')
    msg_box.send_keys(msg)
    driver.find_element_by_class_name('_35EW6').click()  # click en enviar

    end = True

    while end:

        print('Menu (elige una opcion)')
        print('1) Escribir nuevo mensaje')
        print('2) Comprobar mensajes')
        print('3) Cambiar destinatario')
        print('4) salir')
        option = int(input())

        if option==1:
            try:
                user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                user.click()

                msg_box = driver.find_element_by_class_name('_2S1VP')
            except:
                print("Error de version:actualiza el repositorio")

            msg = input('Escribe el mensaje: ')
            msg_box.send_keys(msg)
            driver.find_element_by_class_name('_35EW6').click()#click en enviar
        elif option == 2:
            pass #funcion comprobar correo
        elif option == 3:
            end=send_msg()
        elif option == 4:
            end=False
        else:
            print('Error: opcion no valida')

    return end


#
# for i in range(count):
#     msg_box.send_keys(msg)
#     driver.find_element_by_class_name('_35EW6').click()

if __name__ == '__main__':
    input('Escanea el codigo QR y pulsa enter')


    end = True

    while(end):
        print('Menu (elige una opcion)')
        print('1) elegir destinatario')
        print('2) salir')

        option = int(input())
        if(option==1):
            end = send_msg()
        elif(option==2):
            end=False
        else:
            print('Error: opcion no valida')