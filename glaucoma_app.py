# Modules
import pyrebase
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np


from datetime import datetime

# Configuration Key

firebaseConfig = {
    'apiKey': "AIzaSyD2Evc1iBwghGCUwSFhBruaTMOWU9sehnA",
    'authDomain': "glaucoma-ben.firebaseapp.com",
    'projectId': "glaucoma-ben",
    'databaseURL': "https://glaucoma-ben-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "glaucoma-ben.appspot.com",
    'messagingSenderId': "638260342283",
    'appId': "1:638260342283:web:4dc7f8773c407d2276a10e",
    'measurementId': "G-HPNTPZRMWC"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
st.sidebar.title("Glaucoma app")

# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')

# App

# Sign up Block
# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input(
        'Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        if email is None:
            st.warning('please provide an email')
        elif password is None:
            st.warning('please provide a password')
        else:
            st.success('Your account is created succesfully!')
            st.snow()
            # Sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome' + handle)
            st.info('Login via login drop down selection')


# Login Block
if choice == 'Login':
    if email is None:
        st.warning('please provide an email')
    elif password is None:
        st.warning('please provide a password')
    else:
        login = st.sidebar.checkbox('Login')
        if login:
            user = auth.sign_in_with_email_and_password(email, password)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            bio = st.radio('Jump to', ['Home', 'Glaucoma App', 'Feedback'])

            # SETTINGS PAGE
            if bio == 'Home':
                # CHECK FOR IMAGE
                print('glaucoma')
            # HOME PAGE
            elif bio == 'Glaucoma App':
                st.set_option('deprecation.showfileUploaderEncoding', False)


                # @st.cache(suppress_st_warning=True,allow_output_mutation=True)
                def import_and_predict(image_data, model):
                    image = ImageOps.fit(image_data, (100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    image = np.asarray(image)
                    st.image(image, channels='RGB')
                    image = (image.astype(np.float32) / 255.0)
                    img_reshape = image[np.newaxis, ...]
                    prediction = model.predict(img_reshape)
                    return prediction


                model = tf.keras.models.load_model('my_model2.h5')

                st.write("""
                             # ***Glaucoma detector***
                             """
                         )

                st.write(
                    "This is a simple image classification web app to predict glaucoma through fundus image of eye")

                file = st.file_uploader("Please upload an image(jpg) file", type=["jpg"])

                if file is None:
                    st.text("You haven't uploaded a jpg image file")
                else:
                    imageI = Image.open(file)
                    prediction = import_and_predict(imageI, model)
                    pred = prediction[0][0]
                    if (pred > 0.5):
                        st.write("""
                                     ## **Prediction:** You eye is Healthy. Great!!
                                     """
                                 )
                        st.balloons()
                    else:
                        st.write("""
                                     ## **Prediction:** You are affected by Glaucoma. Please consult an ophthalmologist as soon as possible.
                                     """
                                 )
                        st.error('Glaucoma Positive')




            else:
                st.header(":Hurray!")

                contact_form = """
                    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSeuLuq6uGp0oZ3JMQ_6WdN5cMquDJfDwtlRKY7HAsGtNRNhww/viewform?embedded=true" width="740" height="909" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></form>
                    """

                st.markdown(contact_form, unsafe_allow_html=True)
