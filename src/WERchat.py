#*-----------------------------------------------------------------------------------------------------------------------------------------------
#* WERchat
#*
#* UADER
#* FCyT
#* I+D Resolución “CS” N° 342/23 UADER
#* PI-B FCyT “Plataforma para el despliegue rápido de metodologías ágiles en PyMES y micro - PyMES”
#*
#* Script to process software requirements disambiguation queries to OpenAI ChatCPT
#* remember to process export OPENAI_API_KEY={your OPEN_API_KEY} before executing this script
#*-----------------------------------------------------------------------------------------------------------------------------------------------
from openai import OpenAI
import sys
from datetime import datetime
import time
import os
import re    

# Getting the current date and time
start_time = time.time()
dt = datetime.now()
ts = datetime.timestamp(dt)


#*--- Extract filename to process from arguments
n=len(sys.argv)
script=sys.argv[0]
os.system("clear")
print("\nProcessing %s arguments(%d) %s\n" % (script,n,dt))
if n<2:
	print("Requirements file not informed, exit\n")
	exit(0)
reqtxt=sys.argv[1]
print("Processing requirements file(%s)\n" % (reqtxt))
print("\n========================================================================================================================")
# Opening connection with OpenAI
client = OpenAI()

context="Tu eres un joven, inteligente, muy meticuloso, ordenado y exhaustivo ingeniero de software al que le han asignado la dificil tarea de identificar ambiguedades en los requerimientos de un aplicativo"
usertask="Identifica y enumera las ambiguedades que puedan encontrarse mediante la lectura del siguiente requerimiento"
userquery="Como usuario del sistema quiero visualizar  los datos primarios de comercio para dar el alta.El objetivo de la historia es visualizar los datos del comercio en el sistema, estos datos viene precargados y el usuario podrá modificar algunos y otros no. El usuario tendrá la posibilidad de confirmar esos datos o cancelarlos. Los criterios de aceptación serán como PF quiero visualizar los datos primarios (CUIT, Nombre, Apellido, Nombre de Fantasía) de mis datos cargados en el banco para confirmar la adhesión. Los datos CUIT/CUIL, Nombre, Apellido no se podrán editar.El dato Nombre de Fantasía mostrara la concatenación de nombre y apellido dando la posibilidad al usuario de cambiar ese nombre. El dato eMail estará en blanco y tendrá que ser cargado por el cliente. Cuando todos las datos estén cargados, recién ahí se habilita el botón Continuar"


#open and read requirement file in read mode
outfile, extension = os.path.splitext(reqtxt)
try:
  reqfile = open(reqtxt, "r")
except:
  print("%s Requirement file %s not found\n"%(script,reqtxt))
  exit(0)

userquery = reqfile.read()
reqfile.close()

print(userquery)

print("\n========================================================================================================================")
response = client.chat.completions.create(
  model="gpt-4-0125-preview",
  messages=[
    {
      "role": "system",
      "content": context },
    {
      "role": "user", 
      "content" : usertask },
    {
      "role": "user",
      "content": userquery }

  ],
  temperature=1,
  max_tokens=4096,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response.choices[0].message.content)

#*---- Execution statistics
print("\n========================================================================================================================")
findings=re.findall('\n[0-9]\. ',response.choices[0].message.content )
nfindings=len(findings)

print("%s chatGPT file(%s) model(%s) usage prompt(%s) completion(%s) total(%s)" % (script,reqtxt,response.model,response.usage.prompt_tokens,response.usage.completion_tokens,response.usage.total_tokens))
print("%s input query len(%d)" % (script,len(userquery)))
print("%s output len(%d) findings(%d)" % (script,len(response.choices[0].message.content),nfindings))
print("Findings --> ",findings)
lap=time.time() - start_time
lap=str(lap)
lap=lap.replace(".",",")
print("%s execution time %s secs length(%d)" % (script,lap,len(response.choices[0].message.content)))


#*--- Create a tracelog of the execution
# Append-adds at last
logname, extension = os.path.splitext(script)
logfile = open(logname+".txt", "a")  # append mode
logfile.write("%s,%s,\"%s\",%s,%d,%d,%d,%s,%s,%s,%s\n" % (script,dt,lap,outfile,len(userquery),len(response.choices[0].message.content),nfindings,response.model,response.usage.prompt_tokens,response.usage.completion_tokens,response.usage.total_tokens))
logfile.close()

inname, extension = os.path.splitext(script)
infile = open(inname+".lst", "a")  # append mode
infile.write("*********************************************[%s]**********************************************\n" % (reqtxt))
infile.write("%s\n" % (userquery))
infile.close()


