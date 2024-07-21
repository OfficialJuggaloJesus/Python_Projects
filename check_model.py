from keras.models import load_model

saved_model = load_model('chatbot_model.h5')
print(saved_model.summary())
