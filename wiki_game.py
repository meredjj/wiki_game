import logging
import numpy as np
import traverse as trv
from urllib.parse import urljoin

class WikiGame:
    words = {}
    vecs = []

    def __init__(self, nlp_model_path=None) -> None:
        logging.basicConfig(format='%(asctime)s - %(message)s', 
                            level=logging.INFO)
        self.load_word2vec(nlp_model_path)

    def load_word2vec(self, nlp_model) -> None:
        if nlp_model is None:
            logging.info("No word2vec model specified.")
        else:
            logging.info("Loading word2vec model. This may take a few minutes...")
            words = {}
            vecs = []
            with open(nlp_model, encoding='utf-8') as f:
                f.readline()
                line = f.readline()
                index = 0
                while len(line) > 0:
                    line = line.split(' ')
                    words[line[0]] = index
                    vecs.append(np.array([float(x) for x in line[1:]]))
                    index += 1
                    line = f.readline()

            vecs = np.vstack(vecs)

            self.words = words
            self.vecs = vecs
            logging.info("Done loading word2vec model.")

    def interactive_loop(self):
        logging.info("_____ Playing the wiki-game _____")
        logging.info("Press ctrl-c at any time to quit.")
        logging.info("_________________________________")
        selection = input("Run 1-Random or 2-NLP model (enter 1 or 2): ")
        playing = True
        while playing:
            try:
                if selection == '1':
                    try:
                        start_page = input("Enter a start page: ")
                        target_page = input("Enter a target page: ")
                        running = True
                        while running:
                            trv.random_solve(start_page, target_page)
                            running = False
                    except KeyboardInterrupt:
                        pass
                elif selection == '2':
                    try:
                        start_page = input("Enter a start page: ")
                        target_page = input("Enter a target page: ")
                        running = True
                        while running:
                            trv.nlp_solve(start_page, target_page,
                                           self.words, self.vecs)
                            running = False
                    except KeyboardInterrupt:
                        pass
                else:
                    selection = input("Invalid selection, retry: ")
                    
                selection = input("Run 1-Random or 2-NLP model (enter 1 or 2): ")
            except KeyboardInterrupt:
                playing = False

def main():
    wg = WikiGame(nlp_model_path="./en_wiki_word2vec.txt")
    wg.interactive_loop()

if __name__ == "__main__":
    main()