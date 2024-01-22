from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import cv2
import numpy as np
from .models import PeopleCount
from .models import ResultadoEnquete
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def salvar_resultado_enquete(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        option = data.get('option')

        # Atualizar o modelo no banco de dados
        resultados = ResultadoEnquete.objects.first()
        setattr(resultados, option, getattr(resultados, option) + 1)
        resultados.total += 1
        resultados.save()

        return JsonResponse({'success': True, 'total': resultados.total, 'bemVida': resultados.bemVida, 'grill': resultados.grill, 'modaCasa': resultados.modaCasa, 'receitaChefe': resultados.receitaChefe})

    return JsonResponse({'success': False, 'error': 'Método não permitido'})




def home(request):
  return render(request, 'home.html')

def sua_funcao_de_processamento(request):

  video = cv2.VideoCapture(1)
  verde = False
  amarelo = False
  vermelho = False
  liberado_verde = False
  liberado_amarelo = False
  liberado_vermelho = False
  situacao_fila = ""


  def detectar_pessoas(frame, x, y, w, h):
      # Carregar o classificador pré-treinado para detecção de rosto
      classificador_rosto = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

      # Obter a região de interesse (ROI) da imagem
      roi = frame[y:y + h, x:x + w]

      # Converter para escala de cinza para o classificador Haar Cascade
      roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

      # Detectar rostos na ROI
      rostos_encontrados = classificador_rosto.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5)

      # Desenhar retângulos ao redor dos rostos detectados
      for (rx, ry, rw, rh) in rostos_encontrados:
          cv2.rectangle(roi, (rx, ry), (rx + rw, ry + rh), (255, 0, 0), 2)

      # Se pelo menos um rosto foi detectado, retornar True
      return len(rostos_encontrados) > 0


  # Loop infinito para rodar o vídeo da Webcam

  while True:
      ret,img = video.read()
      # Redimensionamento da imagem
      img = cv2.resize(img,(1280,720),)
      # Aplicação para escala de Gray
      imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
      # Conversão para binário
      imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
      # Expandir imagem para potencializar características
      kernel = np.ones((8,8), np.uint8)
      imgDil = cv2.dilate(imgTh,kernel,iterations=2)

      # Área Verde

      # Medidas da área demarcada
      x_verde, y_verde, w_verde, h_verde = 800, 200, 206, 375
      recorte_verde = imgDil[y_verde:y_verde+h_verde,x_verde:x_verde+w_verde]
      # Quantidade de pixels brancos no espaço
      brancos_verde = cv2.countNonZero(recorte_verde)

      # Chamar função para detectar pessoas no espaço
      analise_verde = detectar_pessoas(img, 800, 200, 206, 375)

      if analise_verde == True:
          verde = True
          liberado_verde = True
      else:
          liberado_verde = False
          verde = False

      # Mudança de cor caso detectado (cinza ou verde)
      if analise_verde == False:
          cv2.rectangle(img, (x_verde, y_verde), (x_verde + w_verde, y_verde + h_verde), (128, 128, 128), 4)
      else:
          cv2.rectangle(img,(x_verde,y_verde),(x_verde+w_verde,y_verde+h_verde),(0, 255, 0),4)

      cv2.rectangle(imgTh, (x_verde, y_verde), (x_verde + w_verde, y_verde + h_verde), (255, 255, 255), 6)

      # Área Amarela

      # Medidas da área demarcada
      x_amarelo, y_amarelo, w_amarelo, h_amarelo = 500, 200, 280, 375
      recorte_amarelo = imgDil[y_amarelo:y_amarelo+h_amarelo,x_amarelo:x_amarelo+w_amarelo]
      # Quantidade de pixels brancos no espaço
      brancos_amarelo = cv2.countNonZero(recorte_amarelo)

      # Chamar função para detectar pessoas no espaço
      analise_amarelo = detectar_pessoas(img, 500, 200, 280, 375)

      if analise_amarelo == True:
          amarelo = True
          liberado_amarelo = True
      else:
          liberado_amarelo = False
          amarelo = False

      # Mudança de cor caso detectado (cinza ou amarelo)
      if analise_amarelo == False:
          cv2.rectangle(img, (x_amarelo, y_amarelo), (x_amarelo + w_amarelo, y_amarelo + h_amarelo), (128, 128, 128),4)
      else:
          cv2.rectangle(img, (x_amarelo, y_amarelo), (x_amarelo + w_amarelo, y_amarelo + h_amarelo), (0, 255, 255),4)

      cv2.rectangle(imgTh, (x_amarelo, y_amarelo), (x_amarelo + w_amarelo, y_amarelo + h_amarelo), (255, 255, 255), 6)

      # Área Vermelha

      # Medidas da área demarcada
      x_vermelho, y_vermelho, w_vermelho, h_vermelho = 130, 200, 350, 375
      recorte_vermelho = imgDil[y_vermelho:y_vermelho + h_vermelho, x_vermelho:x_vermelho + w_vermelho]
      # Quantidade de pixels brancos no espaço
      brancos_vermelho = cv2.countNonZero(recorte_vermelho)

      # Chamar função para detectar pessoas no espaço
      analise_vermelho = detectar_pessoas(img, 130, 200, 350, 375)

      if analise_vermelho == True:
          vermelho = True
          liberado_vermelho = True
      else:
          liberado_vermelho = False
          vermelho = False

      # Mudança de cor caso detectado (cinza ou vermelho)
      if analise_vermelho == False:
          cv2.rectangle(img, (x_vermelho, y_vermelho), (x_vermelho + w_vermelho, y_vermelho + h_vermelho), (128, 128, 128),4)
      else:
          cv2.rectangle(img, (x_vermelho, y_vermelho), (x_vermelho + w_vermelho, y_vermelho + h_vermelho), (0, 0, 255),4)

      cv2.rectangle(imgTh, (x_vermelho, y_vermelho), (x_vermelho + w_vermelho, y_vermelho + h_vermelho), (255, 255, 255), 6)

      # Exibir informações Verde
      cv2.putText(img,str(brancos_verde),(x_verde-10,y_verde-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
      cv2.putText(img, str(verde), (x_verde+110, y_verde-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)

      # Exibir informações Amarelo
      cv2.putText(img, str(brancos_amarelo), (x_amarelo-10, y_amarelo-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
      cv2.putText(img, str(amarelo), (x_amarelo + 110, y_amarelo - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)

      # Exibir informações Vermelho
      cv2.putText(img, str(brancos_vermelho), (x_vermelho - 10, y_vermelho - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
      cv2.putText(img, str(vermelho), (x_vermelho + 110, y_vermelho - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)

      # Condição da Fila
      if liberado_verde and liberado_amarelo and liberado_vermelho == True:
          # Caso ocupado por pessoas, exibir vermelho.
          cv2.rectangle(img, (575, 30), (575 + 250, 30 + 85), (0, 0, 255), -1)
          cv2.putText(img,'Fila em Vermelho', (575, 30 + 85 // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
          situacao_fila = "Vermelho"
          # Extrair dados para situação da fila
          PeopleCount.objects.create(situacao_fila_banco=situacao_fila)
          
      elif liberado_verde and liberado_amarelo == True:
          # Caso ocupado por pessoas, exibir amarelo.
          cv2.rectangle(img, (575, 30), (575 + 250, 30 + 85), (0, 255, 255), -1)
          cv2.putText(img, 'Fila em Amarelo', (575, 30 + 85 // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
          situacao_fila = "Amarelo"
          # Extrair dados para situação da fila
          PeopleCount.objects.create(situacao_fila_banco=situacao_fila)
          
      else:
          # Caso não ocupado ou apenas na área verde, exibir verde.
          cv2.rectangle(img, (575, 30), (575 + 250, 30 + 85), (0, 255, 0), -1)
          cv2.putText(img, ' Fila em Verde', (575, 30 + 85 // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
          situacao_fila = "Verde"
          # Extrair dados para situação da fila
          PeopleCount.objects.create(situacao_fila_banco=situacao_fila)
          

      cv2.imshow('video original',img)
      key = cv2.waitKey(20)

      # Tecla ESC para fechar
      if key == 27:
          break
     
 
  situacao_fila = "Conteúdo da situacao_fila"
  return render(request, 'sua_template.html', {'situacao_fila': situacao_fila})


#Leitura da Webcam
