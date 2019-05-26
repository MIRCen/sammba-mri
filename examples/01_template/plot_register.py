"""
Registration to common space
============================

Here we show how to create a template from multiple anatomical scans and
register all of them to it.
Initially, registration is of extracted brains. Once these are reasonably
aligned, whole heads are registered, weighted by masks that, if parameters
are chosen well, include some scalp. The amount of scalp is hopefully enough
to help in differentiating the brain-scalp boundary without including so much
head tissue that it starts to contaminate the registration with the highly
variable head tissue.
"""
##############################################################################
# Retrieve the data
# -----------------
from sammba import data_fetchers

lemur = data_fetchers.fetch_lemur_mircen_2019_t2(subjects=[0, 1, 2])

##############################################################################
# retest contains paths to images and data description
print(lemur.anat)

##############################################################################
# Define the writing directory
# ----------------------------
import os

write_dir = os.path.join(os.getcwd(), 'lemur_common')
if not os.path.exists(write_dir):
    os.makedirs(write_dir)

##############################################################################
# Create the template
# -------------------
from sammba.registration import anats_to_common

affine_register = anats_to_common(lemur.anat, write_dir, 400,
                                  use_rats_tool=False, caching=True)

##############################################################################
# We set caching to True, so that the computations are not restarted.
# The paths to the registered images can be accessed easilly
registered_anats = affine_register.registered
print(registered_anats)

##############################################################################
# Assess the template
# -------------------
from nilearn import image
template_img = image.mean_img(registered_anats)

##############################################################################
# Visalize results
# ----------------
# We plot the edges of one individual anat on top of the average image
from nilearn import plotting

average_img = image.mean_img(registered_anats)
display = plotting.plot_anat(average_img, dim=-1.6, title='affine register')
display.add_edges(registered_anats[0])
plotting.show()

##############################################################################
# Visualize pipeline steps
# -------------------------
from sammba.graphs import create_pipeline_graph

graph_file = os.path.join(write_dir, 'affine_registration_graph')
create_pipeline_graph('anats_to_common_affine', graph_file)
