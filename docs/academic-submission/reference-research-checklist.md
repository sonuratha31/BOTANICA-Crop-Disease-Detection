# Verified Reference Research

The sources below were checked against a primary publisher/research page,
official framework documentation, or bibliographic metadata for the cited
work. The citations and the claims they support are reproduced in
[report.md](./report.md). Access date for web sources: 19 November 2026.

## Primary research

| Authors | Year | Title and publisher | DOI / official URL | Supports |
| --- | ---: | --- | --- | --- |
| Sharada P. Mohanty, David P. Hughes, Marcel Salathé | 2016 | “Using Deep Learning for Image-Based Plant Disease Detection.” *Frontiers in Plant Science*, 7, article 1419. | [DOI](https://doi.org/10.3389/fpls.2016.01419); [publisher full text](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2016.01419/full) | PlantVillage image dataset context, class count, and prior crop-disease classification research. |
| Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, Liang-Chieh Chen | 2018 | “MobileNetV2: Inverted Residuals and Linear Bottlenecks.” *2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pp. 4510-4520. | [DOI](https://doi.org/10.1109/CVPR.2018.00474); [OpenAlex bibliographic record](https://api.openalex.org/works/https://doi.org/10.1109/CVPR.2018.00474) | Original MobileNetV2 architecture. |
| Ramprasaath R. Selvaraju, Michael Cogswell, Abhishek Das, Ramakrishna Vedantam, Devi Parikh, Dhruv Batra | 2017 | “Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization.” *Proceedings of the IEEE International Conference on Computer Vision*, pp. 618-626. | [DOI](https://doi.org/10.1109/ICCV.2017.74); [CVF Open Access paper page](https://openaccess.thecvf.com/content_iccv_2017/html/Selvaraju_Grad-CAM_Visual_Explanations_ICCV_2017_paper.html); [OpenAlex bibliographic record](https://api.openalex.org/works/https://doi.org/10.1109/ICCV.2017.74) | Original Grad-CAM method and proceedings metadata. |
| David P. Hughes and Marcel Salathé | 2015 | “An open access repository of images on plant health to enable the development of mobile disease diagnostics.” arXiv:1511.08060. | [arXiv record](https://arxiv.org/abs/1511.08060); [DOI](https://doi.org/10.48550/arXiv.1511.08060); [OpenAlex record](https://api.openalex.org/works/https://doi.org/10.48550/arXiv.1511.08060) | PlantVillage image repository context. This is a preprint/repository record. |
| Konstantinos P. Ferentinos | 2018 | “Deep learning models for plant disease detection and diagnosis.” *Computers and Electronics in Agriculture*, 145, 311-318. | [DOI](https://doi.org/10.1016/j.compag.2018.01.009); [OpenAlex bibliographic record](https://api.openalex.org/works/https://doi.org/10.1016/j.compag.2018.01.009) | Related plant-disease deep-learning research. Its reported experimental settings are not directly comparable with BOTANICA. |

## Official framework and application documentation

| Author / organization | Year/version | Title | Official URL | Supports |
| --- | --- | --- | --- | --- |
| François Chollet / Keras | Undated living guide (accessed 2026-11-19) | “Transfer learning & fine-tuning.” TensorFlow/Keras guide. | [TensorFlow guide](https://www.tensorflow.org/guide/keras/transfer_learning) | Frozen pretrained feature extractor and task-specific head as a transfer-learning pattern. |
| TensorFlow Authors | Current API documentation (accessed 2026-11-19) | `tf.keras.applications.MobileNetV2` | [API reference](https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNetV2) | Official MobileNetV2 API and implementation description; links to the original paper. |
| TensorFlow Authors | Current API documentation (accessed 2026-11-19) | `tf.keras.utils.image_dataset_from_directory` | [API reference](https://www.tensorflow.org/api_docs/python/tf/keras/utils/image_dataset_from_directory) | Folder-based dataset loading, integer labels, and validation split parameters. |
| TensorFlow Authors | Current API documentation (accessed 2026-11-19) | `tf.keras.applications.mobilenet_v2.preprocess_input` | [API reference](https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2/preprocess_input) | MobileNetV2 preprocessing and scaling pixel values to [-1, 1]. |
| Streamlit | Current API documentation (accessed 2026-11-19) | `st.cache_resource` and “Caching overview.” | [API](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource); [overview](https://docs.streamlit.io/develop/concepts/architecture/caching) | Caching shared resource objects such as machine-learning models. |
| Streamlit | Current API documentation (accessed 2026-11-19) | `st.file_uploader` and `st.download_button`. | [Uploader API](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader); [download API](https://docs.streamlit.io/develop/api-reference/widgets/st.download_button) | Official upload and download widget behavior. |

## Verification notes

- The Frontiers publisher page was fetched and checked for the PlantVillage
  paper's title, author names, date, journal, DOI, image count, and 38-class
  description.
- The CVF ICCV 2017 Open Access page was opened and checked for the Grad-CAM
  paper's exact title, author order, conference, and page range. Its DOI
  metadata was also checked in OpenAlex.
- The MobileNetV2 paper's title, author names, year, CVPR venue, page range,
  and DOI were checked in OpenAlex metadata, against its DOI record, and
  through the TensorFlow API page's reference link to the original paper.
  The CVPR Open Access page itself was unavailable in the browser during
  this pass.
- The Hughes and Salathé preprint record's title, author names, year, and
  DOI were checked in OpenAlex metadata. The arXiv page itself was
  unavailable to the page fetcher during this pass.
- The Ferentinos article's title, author, journal, volume, pages, year, and
  DOI were checked in OpenAlex bibliographic metadata. The publisher page
  was not accessible through the available fetcher.
- TensorFlow and Streamlit API references were fetched from their official
  documentation sites. Documentation URLs are living pages and may change.
- Mohanty et al. report 54,306 images; the project's current local inventory
  has 54,305. The reason for the one-image difference has not been
  established.
- These citations do not establish the license terms of the local dataset.
  Confirm the actual dataset source and its reuse terms before redistribution.

## Remaining optional research

The core requested sources and related studies are present. A wider
literature survey on
field-image generalization, domain shift, calibration, evaluation design,
and crop-specific management guidance would improve a final thesis, but no
such unsupported claims are added to this report. Add further sources only
after verifying their exact records and relevance.
