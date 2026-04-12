# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---
FindBeats

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

It recommends songs based on a given genre, energy level, mood, and acosuticness, and this is intended for real users because its based on how real recommenders work. 

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

The features and user preferences used are genre, energy, mood, and acousticness.  The model updates the score by +2 points if genre matches, +1 point if mood matches, and how close a song's energy is to what the user prefers, which falls in a range from 0 -1. And if acousticness is true, score goes up by 1 point. 

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

There are 18 songs in the catalog. Some genres include lofi, rofi, pop, classical, r&b, j pop etc. Some moods include happy, relaxed, sad, nostalgic etc. I added 8 more songs to the starter catalog. There are some moods missing like energetic, bittersweet etc. But other than that, I think its comprehensive.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

It works well with genres and moods already in the dataset, for example lofi, which is the genre that is the most common. A pattern the scoring capturs correctly is increasing the score by 2 points if genre matches, because this is most dominant criteria that determines song preferences even in real recommenders. In profile 4, because reggae was not a genre in the dataset, the system went with listing songs that had a mood of happy, which made sense because it was the second most important criteria.

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

One strong weakness if that genre overpowers the other categories so much so that even if the song doesn't have matching mood or energy, it will still recommend that song if the genre matches because of the +2 points it gets because of matching genre. When the 1st profile was tested, with energy 0.9, mood: sad, and genre: lofi, the top 3 results were lofi songs which highlights that genre takes preference over mood and energy, which can be misleading. Although energy of 0.9 and a sad mood was requested, these requests were not taken into consideration. 

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---
I tested 5 user profiles that I mentioned in README.md. I was surprised by how genre completed dominated mood and energy in profile 1 and how acousticness also dominated. In profile 3, even though genre was specificed to be electronic, it recommended songs which were no where close to being electronic but had high acousticness. In profile 4 and 5, a genre and mood was included that were not even included in the dataset, and the recommendations completely failed to notice these discrepancies.

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

I would add a checking statement that would check if a favorite genre or favorite mood is provided, and if not, then it would print an error message, because if the dataset doesn't have a genre or mood that matches, it doesn't make sense to provide recommendations that are nowhere close to what the user wants. I would also had a language preference option so users get recommended songs with that specific language. 

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned about the various ways different recommending systems work and gained a more in-depth idea of how real recommeders work and the detail and thought it requires to come up with a fair scoring system. Using AI tools helped immensely with understanding the codebase and how to develop an algorithm that would be able to recommend songs. I did have to double check it when I asked about the Mermaid.js design, because it did not include energy levels the first time, it added genre, mood, and tempo. I would try to add an option for the user to specific language of the songs they prefer so it can be more personalized. I was surpised about how simply assigning genre to be +2 points could make it feel like a recommendation system because it was prioritizing that over the other features.
