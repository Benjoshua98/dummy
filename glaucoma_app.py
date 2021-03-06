# Modules
import pyrebase
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import requests

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
st.sidebar.title("Glaucoma app")

# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')
st.sidebar.write('Tick the login box as database is a free version one the premiuim features are not in use')
# App

# Sign up Block
# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input(
        'Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created successfully!')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + handle)
        st.info('Login via login drop down selection')

# Login Block
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        bio = st.radio('Jump to', ['Home', 'Glaucoma App', 'Feedback'])
        # SETTINGS PAGE
        if bio == 'Home':


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
                    st.write("[Animation Credits >](https://lottiefiles.com/search?q=eye&category=animations)")

            # ---- HEADER SECTION ----
            with st.container():
                st.write("---")
                st.header('What is Glaucoma?')
                st.subheader(
                    "- a **_group_** of **_eye_** **_diseases_** that affects the **_retina_** and **_weakens the nerve cells_** that assist in visual recognition.")
                st.subheader("- The second highest cause of Irreversible blindness in the world.")
                st.subheader("- Doesn???t have a permanent cure.")

                st.write("[Learn More >](https://www.glaucomapatients.org/)")
                col1, col2 = st.columns((2, 1))
                with col2:
                    st.write("---")

                    st.subheader("Normal")
                    st.subheader("vs")
                    st.subheader("Glaucoma eye")
                with col1:
                    st.image("images/img2.jpg")
                st.write("[Image Credits >](https://tinyurl.com/bew12155)")
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
                            st.write("[Video Credits >](https://glaucoma.org/learn-about-glaucoma/)")

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
                st.write("[Learn More >](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7769798/)")

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

            st.title("""
                                     # ***GlaucoCheck***
                                     """
                     )

            st.header("Welcome to glaucoCheck. Check your eye here.")


            file = st.file_uploader("Please upload an image(jpg) file", type=["jpg"])

            if file is None:
                st.text("You haven't uploaded a jpg image file")
            else:
                imageI = Image.open(file)
                prediction = import_and_predict(imageI, model)
                pred = prediction[0][0]
                if (pred > 0.5):
                    st.write("""
                                             ## **Prediction:** The Person's eye is Healthy. Great!! Tested Negative for Glaucoma
                                             """
                             )
                    st.balloons()
                else:
                    st.write("""
                                             ## **Prediction:** The Person is affected by Glaucoma. Please consult an ophthalmologist as soon as possible. Tested Positve for Glaucoma
                                             """
                             )





        else:
            st.header("Welcome to feedback section")

            contact_form = """
                            <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSeuLuq6uGp0oZ3JMQ_6WdN5cMquDJfDwtlRKY7HAsGtNRNhww/viewform?embedded=true" width="740" height="909" frameborder="0" marginheight="0" marginwidth="0">Loading???</iframe></form>
                            """

            st.markdown(contact_form, unsafe_allow_html=True)
