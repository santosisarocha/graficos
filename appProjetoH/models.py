from django.db import models 
import datetime



    
class PeopleCount(models.Model):
    situacao_fila_banco = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self)-> str:
        return self.situacao_fila_banco
    
    

class ResultadoEnquete(models.Model):
    bemVida = models.IntegerField(default=0)
    grill = models.IntegerField(default=0)
    modaCasa = models.IntegerField(default=0)
    receitaChefe = models.IntegerField(default=0)
    total = models.IntegerField(default=0)



    
 


