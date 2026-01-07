# from engine import run_engine

# if __name__ == "__main__":
#     text = """
#     India has passed a new digital privacy law.
#     The law introduces strict data handling rules for companies.
#     Experts believe this will impact global tech firms operating in India.
#     """

#     result = run_engine(text)

#     print("\n=== RESULT ===")
#     print(result)

curl.exe -X POST http://127.0.0.1:8000/generate-summary `
  -H "Content-Type: application/json" `
  -d '{
    "text": "India passed a new digital privacy law today. The law introduces stricter data handling requirements for companies. Experts believe it will significantly affect global tech firms operating in the country."
  }'


curl.exe -X POST http://127.0.0.1:8000/generate-summary `
  -H "Content-Type: application/json" `
  -d '{
    "text": "Mr.Bum hits the gym everyday and lift weights.He does not skip leg day.He takes rest on SUndays, HE is a gym freak. But he is a good man .He works very hard."
  }'

curl.exe -X POST http://127.0.0.1:8000/generate-summary `
  -H "Content-Type: application/json" `
  -d '{
    "text": "Mr.Bum hits the gym everyday and lift weights.He does not skip leg day.He takes rest on SUndays only."
  }'

"Mr.Bum hits the gym everyday and lift weights.He does not skip leg day.He takes rest on SUndays, HE is a gym freak. But he is a good man .He works very hard."

curl.exe -X POST http://127.0.0.1:8000/generate-summary `
  -H "Content-Type: application/json" `
  -d '{
    "text": "India passed a new digital privacy law today. The law introduces stricter data handling requirements for companies. Experts believe it will significantly affect global tech firms operating in the country."
  }'


"Bali is predominantly a Hindu country. Bali is known for its elaborate, traditional dancing. The dancing is inspired by its Hindi beliefs. Most of the dancing portrays tales of good versus evil. To watch the dancing is a breathtaking experience. Lombok has some impressive points of interest – the majestic Gunung Rinjani is an active volcano. It is the second highest peak in Indonesia. Art is a Balinese passion. Batik paintings and carved statues make popular souvenirs. Artists can be seen whittling and painting on the streets, particularly in Ubud. It is easy to appreciate each island as an attractive tourist destination. Majestic scenery; rich culture; white sands and warm, azure waters draw visitors like magnets every year. Snorkelling and diving around the nearby Gili Islands is magnificent. Marine fish, starfish, turtles and coral reef are present in abundance. Bali and Lombok are part of the Indonesian archipelago. Bali has some spectacular temples. The most significant is the Mother Temple, Besakih. The inhabitants of Lombok are mostly Muslim with a Hindu minority. Lombok remains the most understated of the two islands. Lombok has several temples worthy of a visit, though they are less prolific. Bali and Lombok are neighbouring islands."


curl.exe -X POST http://127.0.0.1:8000/generate-summary `
  -H "Content-Type: application/json" `
  -d '{
    "text": "Bali is predominantly a Hindu country. Bali is known for its elaborate, traditional dancing. The dancing is inspired by its Hindi beliefs. Most of the dancing portrays tales of good versus evil. To watch the dancing is a breathtaking experience. Lombok has some impressive points of interest – the majestic Gunung Rinjani is an active volcano. It is the second highest peak in Indonesia. Art is a Balinese passion. Batik paintings and carved statues make popular souvenirs. Artists can be seen whittling and painting on the streets, particularly in Ubud. It is easy to appreciate each island as an attractive tourist destination. Majestic scenery; rich culture; white sands and warm, azure waters draw visitors like magnets every year. Snorkelling and diving around the nearby Gili Islands is magnificent. Marine fish, starfish, turtles and coral reef are present in abundance. Bali and Lombok are part of the Indonesian archipelago. Bali has some spectacular temples. The most significant is the Mother Temple, Besakih. The inhabitants of Lombok are mostly Muslim with a Hindu minority. Lombok remains the most understated of the two islands. Lombok has several temples worthy of a visit, though they are less prolific. Bali and Lombok are neighbouring islands."
}'