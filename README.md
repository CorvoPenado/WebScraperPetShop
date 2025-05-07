- [CorvoPenado]([https://github.com/seu-usuario](https://github.com/CorvoPenado))  
- [brantst]([https://github.com/usuario-do-colega](https://github.com/brantst))  

# `⛏️DataMiner Pet`
# 🚀 INSTRUÇÕES IMPORTANTES PARA BUILDAR O PROJETO 🚀

---

## 🔴 IMPORTANTE:

1. **NÃO MEXA NO `.spec`!**
   - ❌ **Se você buildar o projeto de outra forma que não seja pelo `.spec` ou pelo `encrypter`, o arquivo `.spec` será excluído automaticamente.**

2. **Por que usar o `encrypter`?**
   - ✔️ Buildar o projeto pelo `encrypter_1.1` ajuda a evitar erros durante o processo e encripta os dados em C e binário. #🔴IMPORTANTE: Ao buildar um executavel sem o `encrypter_1.1` o código fonte *NÂO ESTARÁ ENCRIPTADO*

3. **Ferramentas ou endereçamentos não adaptáveis ao PyInstaller:**
   - 🔧 Se você alterar algo que não seja compatível com o **PyInstaller** ou **Cython**, o projeto pode não funcionar corretamente.

4. **Transferir o ambiente virtual (`venv`) caso baixe o ZIP do projeto completo:**
   - 📦 **Ao fazer o download do projeto em formato ZIP, lembre-se de mover o ambiente virtual (`venv`) para a [pasta principal do projeto](https://github.com/brantst/scraperALPHA/tree/main#-estrutura-correta-do-projeto).**
   - Sem isso, o projeto pode não funcionar corretamente devido à falta de dependências configuradas.


---

## 🛠️ COMO FAZER O BUILDING DO `⛏️DataMiner Pet`:

### 🔹 **Opção 1: Usando o [`encrypter_1.1`](https://github.com/brantst/scraperALPHA/blob/main/encrypter_1.1.exe) (RECOMENDADO)**
Este método é o mais eficaz e reduz a chance de erros de dependências.  

1. ✅ **Marque o `encrypter_1.1` como seguro no Windows Security:**
   - Vá para **Configurações do Windows > Segurança do Windows > Exclusões** e adicione o `encrypter_1.1.exe` como uma exceção.

2. 📂 **Verifique se os arquivos estão nas pastas corretas e se algum arquivo está ausente:**
   - Certifique-se de que  todos os arquivos necessários estão presentes e exatamente nas pastas definidas na [estrutura correta do projeto](https://github.com/brantst/scraperALPHA/tree/main#-estrutura-correta-do-projeto). Arquivos a mais ou faltando, podem e irão causar erros na encriptação.

3. 👨‍💻 **Execute o `encrypter` como Administrador:**
   - Clique com o botão direito no `encrypter_1.1.exe` e escolha **Executar como Administrador**.

4. ❌ **O programa não está rodando corretamente?**
   - Se nada acontecer, é provável que o **Windows esteja bloqueando o arquivo**.
   - Verifique novamente se ele foi adicionado como seguro no **Windows Security** (ou no antivírus).
   - CERTIFIQUE-SE QUE O PASSO 2 ESTÁ DE ACORDO.
   - Verifique se a versão do [encrypter](https://github.com/brantst/scraperALPHA/blob/main/encrypter_1.1.exe) é a mais recente.
   - Visual studio c++ pode não estar atualizado. Verifique a versão https://download.visualstudio.microsoft.com/download/pr/f2819554-a618-400d-bced-774bb5379965/ab3cff3d3a8c48804f47eb521cf138480f5ed4fe86476dd449a420777d7f2ead/vs_BuildTools.exe.

---

### 🔹 **Opção 2: Usando o Prompt de Comando e o PyInstaller**
Se você preferir não usar o `encrypter`, siga este método. **Note que essa opção pode gerar erros de dependências.**
🔴(AO UTILIZAR ESSE MÉTODO O CÓDIGO FONTE NÃO ESTARÁ PROTEGIDO).

1. **Ative o ambiente virtual (`venv`) no prompt de comando:**
   - Abra o terminal na raiz do projeto e execute o comando:
     ```
     petshop/Scripts/activate
     ```

2. **Build o projeto manualmente usando o PyInstaller:**
   - Execute o comando:
     ```
     pyinstaller launcher.spec
     ```

3. **Erros de dependências?**
   - Se o launcher não funcionar após o build, isso pode ser causado por pacotes ou configurações não compatíveis. Use a **Opção 1** para evitar esses problemas.

---

## 📂 ESTRUTURA CORRETA DO PROJETO:

Aqui está a **estrutura completa** do projeto. Organize os arquivos **exatamente** assim:

- **SCRAPER-MAIN/**
  - **app/**
    - **static/**
  - **bot/**
    - [`__init__.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/__init__.py)
    - [`booking.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/booking.py)
    - [`cachorro.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/cachorro.py)
    - [`casa_e_jardim.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/casa_e_jardim.py)
    - [`constants.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/constants.py)
    - [`filtration.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/filtration.py)
    - [`gato.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/gato.py)
    - [`passaro.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/passaro.py)
    - [`peixe.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/peixe.py)
    - [`petily_racao_seca.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/petily_racao_seca.py)
    - [`PetilyHttpSelenium.py`](https://github.com/brantst/scraperALPHA/blob/main/bot/PetilyHttpSelenium.py)
    - outros initializers
  - **petshop/**  (pasta venv)
  - [`encrypter_1.1.exe`](https://github.com/brantst/scraperALPHA/blob/main/encrypter_1.1.exe)
  - [`launcher.py`](https://github.com/brantst/scraperALPHA/blob/main/launcher.py)
  - [`launcher.spec`](https://github.com/brantst/scraperALPHA/blob/main/launcher.spec)
  - [`requirements.txt`](https://github.com/brantst/scraperALPHA/blob/main/requirements.txt)
  - [`setup.py`](https://github.com/brantst/scraperALPHA/blob/main/setup.py)



---

## 📋 Trello:

📌 **Gerencie as tarefas do projeto no Trello:**  
[Trello Board - Projeto Petshop Scrapper](https://trello.com/b/0VCSx9ll/projeto-petshop-scrapper)

---

