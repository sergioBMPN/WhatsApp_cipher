import time
from datetime import datetime as dt
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from random import choice
from cifrado import WhatsAppCipher

class whatsapp:
    def __init__(self, driver):
        self.driver = driver
        self.passwd1 = ''
        self.passwd2 = ''

    def recv_msg(self, name):
        driver = self.driver

        try:
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
            user.click()
            chat_in_container = list()
            tries=0
            while len(chat_in_container)==0 and tries<5:
                time.sleep(1)
                chat_in_container = driver.find_elements_by_xpath(
                    "//div[@class='_3_7SH _3DFk6 message-in' or @class='_3_7SH _3DFk6 message-in tail']")
                tries+=1
            try:
                last_msg_sent = driver.find_elements_by_xpath("//div[@class='_3_7SH _3DFk6 message-out tail']")[-1]
                all_msg_sent = driver.find_elements_by_xpath(
                    "//div[@class='_3_7SH _3DFk6 message-out' or @class='_3_7SH _3DFk6 message-out tail']")

                last_id = last_msg_sent.id
                pos = 0
                for msg in all_msg_sent:
                    if last_id == msg.id:
                        break
                    pos += 1
                last_msg_sent = all_msg_sent[pos:len(all_msg_sent)]#coger los n ultimos mensages

                last_date =''
                for msg in last_msg_sent:
                    msg_container = msg.find_element_by_xpath( ".//div[@class='copyable-text']")
                    last_date= str(msg_container.get_attribute('data-pre-plain-text')).replace("[", "").split("]")[0]
                    print('\t\t\t\t\t\t\t'+(msg_container.text.replace("\n","")+'\t'+last_date))
                last_date=dt.strptime(last_date, "%H:%M,%d/%m/%Y")

            except IndexError:
                last_msg_sent = None
            message = ''
            user = ''
            date = ''
            printed=False
            for messages in chat_in_container:
                try:
                    message_container = messages.find_element_by_xpath(".//div[@class='copyable-text' or @class='_3Usvm copyable-text']")#no tail; tail// tail==nuevo usuario
                    message = message_container.find_element_by_xpath(".//span[@class='selectable-text invisible-space copyable-text']").text

                    date, user = str(message_container.get_attribute('data-pre-plain-text')).replace("[", "").split("]")
                    user = user.replace(":", "").replace("\t", "")
                except NoSuchElementException:
                    try:
                        message_container = messages.find_element_by_xpath(".//div[@class='_3Usvm copyable-text']")
                        message = message_container.find_element_by_xpath(".//img[@class='_2DV1k QkfD1 selectable-text invisible-space copyable-text']").get_attribute("data-plain-text");
                    except NoSuchElementException:
                        pass
                p_date=dt.strptime(date,"%H:%M,%d/%m/%Y")

                if "PWD->" in message:
                    if self.passwd2 == '':
                        self.passwd2 = message.replace("PWD->", "", 1)
                    else:
                        pass
                elif p_date >= last_date:
                    cipher = WhatsAppCipher(self.passwd2)
                    message = cipher.descifrar(message.encode())
                    print(user+': '+message.decode()+'\t'+date)
                    printed=True
            if not printed:
                print("No hay mensajes nuevos")
        except NoSuchElementException:
            print("Error de version:actualiza el repositorio")

        #
        # try:
        #     user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
        #     user.click()
        #     msg_container = driver.find_elements_by_xpath('//span[@class = "{}"]'.format('selectable-text invisible-space copyable-text'))
        #     msg_container1 = driver.find_elements_by_xpath("//div[@class='_3_7SH _3DFk6 message-in']")
        #     msg_container2 = driver.find_elements_by_xpath("//div[@class='_3_7SH _3DFk6 message-in tail']")
        #
        #     for msg in msg_container:
        #         print(msg.text)
        # except:
        #     print("Error de version:actualiza el repositorio")

    def send_msg(self):

        longitud = 16
        valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        name = input('Introduce el nombre de usuario o grupo : ')
        driver = self.driver


        passwd = ""

        passwd = passwd.join([choice(valores) for i in range(longitud)])

        self.passwd1 = passwd
        end = True


        try:
            # encontrar al usuario
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
            user.click()

            # encontrar el cuadro de texto
            msg_box = driver.find_element_by_class_name('_2S1VP')
            msg_box.send_keys('PWD->' + passwd)
            driver.find_element_by_class_name('_35EW6').click()  # click en enviar

            while end:

                print('Menu (elige una opcion)')
                print('1) Escribir nuevo mensaje')
                print('2) Comprobar mensajes')
                print('3) Cambiar destinatario')
                print('4) salir')
                option = int(input())

                if option == 1:
                    try:

                        msg = input('Escribe el mensaje: ')

                        cipher = WhatsAppCipher(passwd)
                        cifrado = cipher.cifrar(msg)

                        msg_box.send_keys(cifrado.decode())
                        driver.find_element_by_class_name('_35EW6').click()  # click en enviar

                    except NoSuchElementException:
                        print("Error de version:actualiza el repositorio")

                elif option == 2:
                    self.recv_msg(name)
                elif option == 3:
                    end = self.send_msg()
                elif option == 4:
                    end = False
                else:
                    print('Error: opcion no valida')

        except NoSuchElementException:
            print("Error de version:actualiza el repositorio")
        return end


#
# for i in range(count):
#     msg_box.send_keys(msg)
#     driver.find_element_by_class_name('_35EW6').click()

if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path='./geckodriver-v0.23.0-linux64/geckodriver')
    driver.get('https://web.whatsapp.com/')
    input('Escanea el codigo QR y pulsa enter')


    whats=whatsapp(driver)

    end = True

    while(end):
        print('Menu (elige una opcion)')
        print('1) Elegir destinatario')
        print('2) Salir')

        option = int(input())
        if(option==1):
            end = whats.send_msg()
        elif(option==2):
            end=False
        else:
            print('Error: opcion no valida')

    driver.close()