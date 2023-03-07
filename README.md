# wiki_game
Solving the wikipedia game using natural language processing models

This repo is meant to showcase a solution to the [Wikipedia Game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game)

It uses a word2vec natural language processing model to score the links on a given page relative to the words in the target page's url.
For my testing, I used a [pre-trained word2vec model (download link)](https://drive.google.com/file/d/12fkBMFubpg5oduN4KCTy5nHlHhOPObKr/view?usp=sharing) that was trained on the English version of Wikipedia.

The goal was to consistently beat the "random case" of randomly selecting links on a page until the target page was found. The random traversal function is also included in the traverse.py file.

## Example Traversal
```
Enter a start page: https://en.wikipedia.org/wiki/Python_(programming_language)
Enter a target page: https://en.wikipedia.org/wiki/Surgeon
found surgeon in model at index 8873
Starting traversal -----
Start page: https://en.wikipedia.org/wiki/Python_(programming_language)
Target page: https://en.wikipedia.org/wiki/Surgeon
https://en.wikipedia.org/wiki/Differentiable_function
https://en.wikipedia.org/wiki/Data_augmentation
https://en.wikipedia.org/wiki/CURE_algorithm
https://en.wikipedia.org/wiki/Proper_generalized_decomposition
https://en.wikipedia.org/wiki/OPTICS_algorithm
https://en.wikipedia.org/wiki/Vision_transformer
https://en.wikipedia.org/wiki/BERT_(language_model)
https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)
https://en.wikipedia.org/wiki/Wharton_School_of_the_University_of_Pennsylvania
https://en.wikipedia.org/wiki/Perelman_School_of_Medicine_at_the_University_of_Pennsylvania
https://en.wikipedia.org/wiki/Surgery
Success! Found your target page in 11 steps
```


Note: There are some cases where the model does not perform well. For example, if the target page is a name or a title that requires context to understand. 

