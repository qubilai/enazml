
import argparse
import os
import numpy as np
import joblib

#from mnist_script.yardimci import veri_uncompress #localde test ederken
from yardimci import veri_uncompress #script klasorunda hepsi bir arada olacak.

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score,recall_score,accuracy_score

from azureml.core import Run

#dışarıdan bu dosyaya arguman gönderebilelim. 
parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
parser.add_argument('--regularization', type=float, dest='reg', default=0.01, help='regularization rate')
#argumanları pars edelim.
args = parser.parse_args()

#data_folder argumanından gelen yolu kullanacağız.
#azure_veri_klasoru = os.path.join(args.data_folder, 'mnist_data')

train_images_path=args.data_folder+'/train-images.gz'
train_labels_path=args.data_folder+'/train-labels.gz'
test_images_path =args.data_folder+'/test-images.gz'
test_labels_path =args.data_folder+'/test-labels.gz'

#veriyi seçelim.
X_train = veri_uncompress(train_images_path, False) / 255.0
y_train = veri_uncompress(train_labels_path, True).reshape(-1)

X_test = veri_uncompress(test_images_path, False) / 255.0
y_test = veri_uncompress(test_labels_path, True).reshape(-1)

#eğitelim
#args.reg dışarıdan arguman ile gelecek ve 0.8 göndereceğiz.
clf = LogisticRegression(C=1/args.reg, solver="liblinear")
clf.fit(X_train, y_train)

#tahmin edelim.
y_test_tahmin = clf.predict(X_test)

#metrikler
prec=precision_score(y_test,y_test_tahmin,average='macro')
rec=recall_score(y_test, y_test_tahmin, average='macro')
acc= accuracy_score(y_test, y_test_tahmin,normalize=True)
print("Precision: {}\nRecall: {}\nAccuracy: {}".format(prec,rec,acc))

#run yakalyalım ve loglara bazı bilgileri yazalım.
run = Run.get_context()

run.log('regularization rate', np.float(args.reg))
run.log('Precision',prec)
run.log('Recall',rec)
run.log('accuracy', acc)

#eğitilen modeli kaydedelim.
os.makedirs('outputs', exist_ok=True)
joblib.dump(value=clf, filename='outputs/sklearn_mnist_trained_model.pkl')
