from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.1", temperature=0)

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for dicphering text snippets. 
    You are given a list of text snippets. These snippets belong to all sorts of sources from various speech of a comic book, to
    menu items of a restaurant menu, to documentation of a scientific paper, etc. These snippets were extracted haphazardly so 
    sometimes two or more snippets are part of the same conversation or sentence. Infer what these snippets mean based on the context.
    Give what you think the source of these text snippets is and summarize what they mean as a whole. Answer this directly and
    do not write without any additional context and limit your answer to 2-3 sentences. 
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Text Snippets: {text_snippets} 
    Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["text_snippets"],
)


def contextualize_text_snippets(text_snippets: List[str], llm=llm, prompt=prompt):
    """
    Given a list of text snippets infer what these snippets mean based on the context.
    Give a brief summary of what the source of these text snippets is and summarize what they mean as a whole.
    """
    rag_chain = prompt | llm | StrOutputParser()
    generation = rag_chain.invoke({"text_snippets": text_snippets})
    return generation
