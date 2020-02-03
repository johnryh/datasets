# coding=utf-8
# Copyright 2019 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DeepLesion dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
import os
import io
from zipfile import ZipFile


# info of deeplesion dataset
_URL = ("https://nihcc.app.box.com/v/DeepLesion")

_DESCRIPTION = """\
The DeepLesion dataset contains 32,120 axial computed tomography (CT) slices 
from 10,594 CT scans (studies) of 4,427 unique patients. There are 1–3 lesions 
in each image with accompanying bounding  boxes  and  size  measurements,  
adding  up  to  32,735  lesions  altogether.  The  lesion annotations were 
mined from NIH’s picture archiving and communication system (PACS).
"""

_CITATION = """\
@article{DBLP:journals/corr/abs-1710-01766,
  author    = {Ke Yan and
               Xiaosong Wang and
               Le Lu and
               Ronald M. Summers},
  title     = {DeepLesion: Automated Deep Mining, Categorization and Detection of
               Significant Radiology Image Findings using Large-Scale Clinical Lesion
               Annotations},
  journal   = {CoRR},
  volume    = {abs/1710.01766},
  year      = {2017},
  url       = {http://arxiv.org/abs/1710.01766},
  archivePrefix = {arXiv},
  eprint    = {1710.01766},
  timestamp = {Mon, 13 Aug 2018 16:48:13 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1710-01766},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""


class Deeplesion(tfds.core.GeneratorBasedBuilder):
  """DeepLesion dataset builder.
  """

  VERSION = tfds.core.Version('0.1.0')

  def _info(self):
    return tfds.core.DatasetInfo(
      builder=self,
      description=_DESCRIPTION,
      features=tfds.features.FeaturesDict({
        "image/name":tfds.features.Text(),
        "image":tfds.features.Image(shape=(None, None, 1), dtype=tf.uint16, encoding_format='png'),
        "bboxs":tfds.features.Sequence(tfds.features.BBoxFeature())
      }),
      homepage=_URL,
      citation=_CITATION,
    )


  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    resources = {
      'zipfile01':'https://nihcc.box.com/shared/static/sp5y2k799v4x1x77f7w1aqp26uyfq7qz.zip',
      'zipfile02':'https://nihcc.box.com/shared/static/l9e1ys5e48qq8s409ua3uv6uwuko0y5c.zip',
      'zipfile03':'https://nihcc.box.com/shared/static/48jotosvbrw0rlke4u88tzadmabcp72r.zip',
      'zipfile04':'https://nihcc.box.com/shared/static/xa3rjr6nzej6yfgzj9z6hf97ljpq1wkm.zip',
      'zipfile05':'https://nihcc.box.com/shared/static/58ix4lxaadjxvjzq4am5ehpzhdvzl7os.zip',
      'zipfile06':'https://nihcc.box.com/shared/static/cfouy1al16n0linxqt504n3macomhdj8.zip',
      'zipfile07':'https://nihcc.box.com/shared/static/z84jjstqfrhhlr7jikwsvcdutl7jnk78.zip',
      'zipfile08':'https://nihcc.box.com/shared/static/6viu9bqirhjjz34xhd1nttcqurez8654.zip',
      'zipfile09':'https://nihcc.box.com/shared/static/9ii2xb6z7869khz9xxrwcx1393a05610.zip',
      'zipfile10':'https://nihcc.box.com/shared/static/2c7y53eees3a3vdls5preayjaf0mc3bn.zip',

      'zipfile11':'https://nihcc.box.com/shared/static/2zsqpzru46wsp0f99eaag5yiad42iezz.zip',
      'zipfile12':'https://nihcc.box.com/shared/static/8v8kfhgyngceiu6cr4sq1o8yftu8162m.zip',
      'zipfile13':'https://nihcc.box.com/shared/static/jl8ic5cq84e1ijy6z8h52mhnzfqj36q6.zip',
      'zipfile14':'https://nihcc.box.com/shared/static/un990ghdh14hp0k7zm8m4qkqrbc0qfu5.zip',
      'zipfile15':'https://nihcc.box.com/shared/static/kxvbvri827o1ssl7l4ji1fngfe0pbt4p.zip',
      'zipfile16':'https://nihcc.box.com/shared/static/h1jhw1bee3c08pgk537j02q6ue2brxmb.zip',
      'zipfile17':'https://nihcc.box.com/shared/static/78hamrdfzjzevrxqfr95h1jqzdqndi19.zip',
      'zipfile18':'https://nihcc.box.com/shared/static/kca6qlkgejyxtsgjgvyoku3z745wbgkc.zip',
      'zipfile19':'https://nihcc.box.com/shared/static/e8yrtq31g0d8yhjrl6kjplffbsxoc5aw.zip',
      'zipfile20':'https://nihcc.box.com/shared/static/vomu8feie1qembrsfy2yaq36cimvymj8.zip',

      'zipfile21':'https://nihcc.box.com/shared/static/ecwyyx47p2jd621wt5c5tc92dselz9nx.zip',
      'zipfile22':'https://nihcc.box.com/shared/static/fbnafa8rj00y0b5tq05wld0vbgvxnbpe.zip',
      'zipfile23':'https://nihcc.box.com/shared/static/50v75duviqrhaj1h7a1v3gm6iv9d58en.zip',
      'zipfile24':'https://nihcc.box.com/shared/static/oylbi4bmcnr2o65id2v9rfnqp16l3hp0.zip',
      'zipfile25':'https://nihcc.box.com/shared/static/mw15sn09vriv3f1lrlnh3plz7pxt4hoo.zip',
      'zipfile26':'https://nihcc.box.com/shared/static/zi68hd5o6dajgimnw5fiu7sh63kah5sd.zip',
      'zipfile27':'https://nihcc.box.com/shared/static/3yiszde3vlklv4xoj1m7k0syqo3yy5ec.zip',
      'zipfile28':'https://nihcc.box.com/shared/static/w2v86eshepbix9u3813m70d8zqe735xq.zip',
      'zipfile29':'https://nihcc.box.com/shared/static/0cf5w11yvecfq34sd09qol5atzk1a4ql.zip',
      'zipfile30':'https://nihcc.box.com/shared/static/275en88yybbvzf7hhsbl6d7kghfxfshi.zip',

      'zipfile31':'https://nihcc.box.com/shared/static/l52tpmmkgjlfa065ow8czhivhu5vx27n.zip',
      'zipfile32':'https://nihcc.box.com/shared/static/p89awvi7nj0yov1l2o9hzi5l3q183lqe.zip',
      'zipfile33':'https://nihcc.box.com/shared/static/or9m7tqbrayvtuppsm4epwsl9rog94o8.zip',
      'zipfile34':'https://nihcc.box.com/shared/static/vuac680472w3r7i859b0ng7fcxf71wev.zip',
      'zipfile35':'https://nihcc.box.com/shared/static/pllix2czjvoykgbd8syzq9gq5wkofps6.zip',
      'zipfile36':'https://nihcc.box.com/shared/static/2dn2kipkkya5zuusll4jlyil3cqzboyk.zip',
      'zipfile37':'https://nihcc.box.com/shared/static/peva7rpx9lww6zgpd0n8olpo3b2n05ft.zip',
      'zipfile38':'https://nihcc.box.com/shared/static/2fda8akx3r3mhkts4v6mg3si7dipr7rg.zip',
      'zipfile39':'https://nihcc.box.com/shared/static/ijd3kwljgpgynfwj0vhj5j5aurzjpwxp.zip',
      'zipfile40':'https://nihcc.box.com/shared/static/nc6rwjixplkc5cx983mng9mwe99j8oa2.zip',

      'zipfile41':'https://nihcc.box.com/shared/static/rhnfkwctdcb6y92gn7u98pept6qjfaud.zip',
      'zipfile42':'https://nihcc.box.com/shared/static/7315e79xqm72osa4869oqkb2o0wayz6k.zip',
      'zipfile43':'https://nihcc.box.com/shared/static/4nbwf4j9ejhm2ozv8mz3x9jcji6knhhk.zip',
      'zipfile44':'https://nihcc.box.com/shared/static/1lhhx2uc7w14bt70de0bzcja199k62vn.zip',
      'zipfile45':'https://nihcc.box.com/shared/static/guho09wmfnlpmg64npz78m4jg5oxqnbo.zip',
      'zipfile46':'https://nihcc.box.com/shared/static/epu016ga5dh01s9ynlbioyjbi2dua02x.zip',
      'zipfile47':'https://nihcc.box.com/shared/static/b4ebv95vpr55jqghf6bthg92vktocdkg.zip',
      'zipfile48':'https://nihcc.box.com/shared/static/byl9pk2y727wpvk0pju4ls4oomz9du6t.zip',
      'zipfile49':'https://nihcc.box.com/shared/static/kisfbpualo24dhby243nuyfr8bszkqg1.zip',
      'zipfile50':'https://nihcc.box.com/shared/static/rs1s5ouk4l3icu1n6vyf63r2uhmnv6wz.zip',

      'zipfile51':'https://nihcc.box.com/shared/static/7tvrneuqt4eq4q1d7lj0fnafn15hu9oj.zip',
      'zipfile52':'https://nihcc.box.com/shared/static/gjo530t0dgeci3hizcfdvubr2n3mzmtu.zip',
      'zipfile53':'https://nihcc.box.com/shared/static/7x4pvrdu0lhazj83sdee7nr0zj0s1t0v.zip',
      'zipfile54':'https://nihcc.box.com/shared/static/z7s2zzdtxe696rlo16cqf5pxahpl8dup.zip',
      'zipfile55':'https://nihcc.box.com/shared/static/shr998yp51gf2y5jj7jqxz2ht8lcbril.zip',
      'zipfile56':'https://nihcc.box.com/shared/static/kqg4peb9j53ljhrxe3l3zrj4ac6xogif.zip',
      'ann_file':'https://raw.githubusercontent.com/anir16293/Deep-Lesion/master/DL_info.csv'
    }

    # download all resources
    archive_paths = dl_manager.download(resources)

    # get ann_file
    ann_path = archive_paths['ann_file']
    del archive_paths['ann_file']

    # build hash table to lookup images
    lut_archive = _build_lut_archive(archive_paths)

    # split anns by `Train_Val_Test`
    train_split, val_split, test_split = _ann_parser(ann_path)

    return [
      tfds.core.SplitGenerator(
        name=tfds.Split.TRAIN,
        gen_kwargs={
          "lut_archive": lut_archive,
          "split": train_split,
        },
      ),
      tfds.core.SplitGenerator(
        name=tfds.Split.VALIDATION,
        gen_kwargs={
          "lut_archive": lut_archive,
          "split": val_split,
        },
      ),
      tfds.core.SplitGenerator(
        name=tfds.Split.TEST,
        gen_kwargs={
          "lut_archive": lut_archive,
          "split": test_split,
        },
      ),
    ]


  def _generate_examples(self, lut_archive, split):
    """Returns examples

    Args:
      lut_archive: `dict`, lookup dictionary to lookup which archive a series_folder belongs to
      split: `dataframe`, annotation information of images

    Yields:
      example key and data
    """
    for idx, value in enumerate(split.values):
      file_name, bboxs, size, sp = value
      record = {
        "image/name": file_name,
        "image": _extract_image(file_name, lut_archive[_parse_fname(file_name)[0]]),
        "bboxs": _format_bboxs(bboxs, size)
      }
      yield idx, record


def _build_lut_archive(paths):
  """Returns dicionary to lookup which archive a series_folder belongs to.

  Args:
    paths: `dict`, <zipfile#>:<path_zipfile>

  Returns:
    `dict`, <series_folder>:<path_zipfile>
  """
  lut = {}
  for k, v in paths.items(): # {<zipfn>:<unzip_path>}
    with ZipFile(v, 'r') as zip:
      for name in zip.namelist():
        series_folder = name.split('/')[1]
        lut[series_folder] = v
  return lut


def _extract_image(fname, archive):
  """Returns a file object from an archive

  Args:
    fname: `string`, file_name in annotation files
    archive: `ZipFile`, path of a zipfile

  Returns:
    file object with the file name
  """
  with ZipFile(archive, 'r') as zip:
    series_folder, slice_fname = _parse_fname(fname)
    fpath = os.path.join('Images_png', series_folder, slice_fname)
    f_obj = io.BytesIO(zip.read(fpath))
  return f_obj

        
def _parse_fname(fname):
  """Returns the series_folder and the name of a slice parsed from given file name

  Args:
    fname: `string`, file_name in annotation files

  Returns:
    tuple of two strings, (series_folder, name of a slice)
  """
  slice_fname = fname.split('_')[-1]
  series_folder = '_'.join(fname.split('_')[:-1])

  return series_folder, slice_fname


def _format_bboxs(bboxs, size):
  """Returns bbox feature

  Args:
    bboxs: `string`, "xmin,ymin,xmax,ymax"
    size: `string`, "height,width", height is assumed to be equal with width.

  Returns:
    tfds.features.BBox
  """
  size = [float(x) for x in size.split(',')]
  if len(size) != 2 or size[0] != size[1]:
      raise AssertionError('height should be equal with width for this dataset')
  coords = np.clip([float(x) for x in bboxs.split(',')], 0.0, size[0])

  cnt = int((len(coords))/4)

  bbox_list = []
  for i in range(cnt):
      ymin = coords[i*4+1] / size[1]
      xmin = coords[i*4] / size[0]
      ymax = coords[i*4+3] / size[1]
      xmax = coords[i*4+2] / size[0]
      bbox_list.append(tfds.features.BBox(ymin=ymin, xmin=xmin, ymax=ymax, xmax=xmax))

  return bbox_list
    
    
def _ann_parser(ann_path):
  """parsers the annotation file and returns the splits in dataframes

  Args:
    ann_path: `string`, path of the annotation file

  Returns:
    tuple with 3 dataframes: (train, validation, test)
  """
  pd = tfds.core.lazy_imports.pandas
  with tf.io.gfile.GFile(ann_path) as csv_f:
      df = pd.read_csv(csv_f)
      df_t = df[['File_name', 'Bounding_boxes', 'Image_size', 'Train_Val_Test']]
      concat = lambda a: ", ".join(a)
      d = {'Bounding_boxes': concat,
           'Image_size':'first',
           'Train_Val_Test':'first'}
      df_new = df_t.groupby('File_name', as_index=False).aggregate(d).reindex(columns=df_t.columns)

      df_train = df_new[df_new['Train_Val_Test']==1]
      df_val = df_new[df_new['Train_Val_Test']==2]
      df_test = df_new[df_new['Train_Val_Test']==3]
  return df_train, df_val, df_test