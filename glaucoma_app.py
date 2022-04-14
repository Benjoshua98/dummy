# Modules
import pyrebase
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import requests
import time

from streamlit_lottie import st_lottie
from PIL import Image
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
st.sidebar.title("Our community app")

# Authentication


# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')

# App

# Sign up Block


# Login Block

login = st.sidebar.button('Login')
if login:
    user = auth.sign_in_with_email_and_password(email, password)
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success('Done!')
    st.snow()

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    bio = st.radio('Jump to', ['Home', 'Glaucoma App', 'Feedback'])

    # SETTINGS PAGE
    if bio == 'Home':
        # Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/

        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()


        # Use local CSS
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


        local_css("style.css")

        # ---- LOAD ASSETS ----
        lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_xa0q7ly3.json")
        # Welcome
        st.title('Welcome to Mission Glaucoma')
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                st.header("No object is mysterious and the mystery is your Eye ")
            with right_column:
                st_lottie(lottie_coding, height=300, key="coding")

        # ---- HEADER SECTION ----
        with st.container():
            st.write("---")
            st.header('what is Glaucoma')
            st.subheader(
                "- an **_eye_** **_problem_** that affects the **_retina_** and **_weakens the nerve cells_** that assist in visual recognition.")
            st.subheader("- The second highest cause of Irreversible blindness in the world.")
            st.subheader("- Doesn’t have a permanent cure.")

            st.write("[Learn More >](https://www.glaucomapatients.org/)")
            col1, col2 = st.columns((2, 1))
            with col2:
                st.write("---")

                st.subheader("Normal")
                st.subheader("vs")
                st.subheader("Glaucoma eye")
            with col1:
                st.image("images/img2.jpg")
            # st.columns
            # st.image("images/img2.jpg",width=500, caption='Normal vs Glaucoma eye')

        # ---- content 1 ----
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                with left_column:
                    st.header("What glaucoma does")

                    st.write("##")
                    st.write(
                        """
                        - Glaucoma is usually, but not always, the result of abnormally high pressure inside your eye called Intraocular Pressure (IOP) .
                        - Slowly damages optic nerve.
                        - Glaucoma initially has no symptoms.
                        - At some point, side (peripheral) vision is lost.
                        - If untreated, an individual can become totally blind for the lifetime.
                        so, Early Detection is the best possible treatment.
                        """
                    )
                    st.write("[.... >](https://www.glaucomapatients.org/basic/definition/)")
                    with right_column:
                        st.header("watch video")

                        st.video("video/vid.mp4", format="video/mp4")

        ## statistics

        images1 = ['stat/glaucomastats.png',
                   'stat/Fig1Projected prevalence of glaucoma.png',
                   'stat/Fig2 Age-specific prevalence of diagnosed glaucoma in 2018.png',
                   'stat/Fig3 gender-specific prevalence of diagnosed glaucoma in 2018.png',
                   ]
        images2 = ['stat/Fig4 Race-specific prevalence of diagnosed glaucoma in 2018.png',
                   'stat/Fig5 Age-specific prevalence of diagnosed glaucoma by ethnic groups in 2018.png',
                   'stat/Fig6 Future projections of POAG glaucoma.png']
        with st.container():
            st.write("---")
            st.header('Statistics')
            left_column, right_column = st.columns(2)
            with left_column:
                st.image(images1, use_column_width=True, caption=images1)
            with right_column:
                st.image(images2, use_column_width=True, caption=images2)

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

        st.write("This is a simple image classification web app to predict glaucoma through fundus image of eye")

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




    else:
        st.header(":Hurray!")

        contact_form = """
                    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSeuLuq6uGp0oZ3JMQ_6WdN5cMquDJfDwtlRKY7HAsGtNRNhww/viewform?embedded=true" width="740" height="909" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></form>
                    """

        st.markdown(contact_form, unsafe_allow_html=True)

else:
    st.write('enter valid email address or password')
