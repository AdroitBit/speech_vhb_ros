import yaml
import re
import rospkg
rospack=rospkg.RosPack()
pkg_dir=rospack.get_path('skuba_ahr_speechprocessing')



class CommandExtractor():
    def __init__(self):
        self.model=None
        self._vectorizer=None
    def load_model(self,datasets_path,debug=False):
        DATA_DIR=datasets_path
        import numpy as np
        import pandas as pd
        df=pd.read_excel(DATA_DIR+'data.xlsx')
        df.sort_values(by=["command","sentence"], inplace = True)
        df.to_excel(DATA_DIR+'data.xlsx', index=False)

        df=pd.read_excel(DATA_DIR+'data.xlsx')
        for i in range(len(df['sentence'])):
            df['sentence'][i]=self.clean_string(df['sentence'][i])
        print(df)

        from sklearn.model_selection import train_test_split
        if debug==True:
            X_train, X_test, y_train, y_test = train_test_split(df['sentence'], df['command'])
        else:
            X_train=df['sentence']
            y_train=df['command']
            for _ in range(3):
                X_train.append(df['sentence'],ignore_index=True)
                y_train.append(df['command'],ignore_index=True)
            #X_train=pd.concat(df['sentence'],df['sentence'])
            #y_train=pd.concat(df['command'],df['command'])
            
            #print(X_train)
        if debug==True:
            len(X_train),len(X_test)


        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer=TfidfVectorizer(stop_words='english',max_features=1000,decode_error='ignore')
        vectorizer.fit(X_train)

        from sklearn.naive_bayes import MultinomialNB
        cls=MultinomialNB()
        cls.fit(vectorizer.transform(X_train),y_train)

        from sklearn.metrics import classification_report,accuracy_score
        if debug:
            y_pred=cls.predict(vectorizer.transform(X_test))
            print(accuracy_score(y_test,y_pred))
            print(classification_report(y_test,y_pred))

        self.model=cls
        self._vectorizer=vectorizer
    def extract(self,s):
        #ex.
        #"Robot please help me carry this luggage" => "carry luggage"
        #"Tomohawk please help me carry this luggage" => "carry luggage"
        #"thank you" => "thank you"
        #"navigate to the nearest airport,please" => "navigate to nearest airport"
        #"I want to go to person,please" => "navigate to person"
        #"Please go to Amber at the toilet" => "go to Amber at toilet"
        if self.model is None:
            return s
        s=self.clean_string(s)
        s_p=self._vectorizer.transform([s])
        s_p=self.model.predict(s_p)[0]
        if s_p=='no extract':
            return s
        
        return s_p
    def clean_string(self,s):
        s=re.sub(r'[^A-Za-z0-9 ]+', ' ', s)
        s=re.sub('  ','',s)
        s=s.strip().lower()
        return s


class WordMapper():
    def __init__(self):
        #self.config_path=data=yaml.safe_load(open(pkg_dir+'/config/sentence-mapper/vosk-GPSR.yaml').read())
        self.config_path=pkg_dir+'/config/word-mapper/vosk-OPL.yaml'
    def map(self,s):
        data=yaml.safe_load(open(self.config_path).read())
        if data is None:
            return s
        for k,v in data.items():
            for i in v:
                s=s.replace(i,k)
        return s