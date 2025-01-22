from flask import Flask, render_template,request, jsonify
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from opencc import OpenCC
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')  # 取得 API 金鑰

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
@app.route('/')
def index():
    return render_template('index.html')

client=OpenAI()


@app.route('/get_response', methods=['POST'])
def get_response():
    # Get user input from request
    user_input = request.form.get('user_input')
    if not user_input:
        return jsonify({'error': 'No user input provided'})
    
    
    embeddings = OpenAIEmbeddings()

    db = Chroma(persist_directory="./db/temp/", embeddings_function=embeddings)
    docs = db.similarity_search(user_input)

    # Initialize the language model
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0.5
    )


    # Load embeddings and search database
    

    # Load QA chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Use OpenAI callback and invoke chain
    with get_openai_callback() as cb:
        response = chain.invoke({"input_documents": docs, "question": user_input}, return_only_outputs=True)

    # Convert simplified Chinese to traditional Chinese
    cc = OpenCC('s2t')
    answer = cc.convert(response['output_text'])

    # Return response
    return jsonify({'response': answer})

    # 啟動伺服器
if __name__ == '__main__':
    app.run(debug=True)



