import argparse

from vqa import vqa
from langsam import run_segmentor
from to_chatgpt import to_chat_gpt


def run_main(args):
    '''
    Not yet functional, but the pipeline would be as follows

    Use VQA or manually enter the objects you see --> 

    Pass them to Chat GPT and receive a tuple/dictionary with object and correct position --> 
    
    pass that to LangSAM for mask arrangment
    
    '''

    image_path = args.image_path

    if args.use_vqa:
        vqa(image_path)
    else: 
        objects = args.objects_present.split(',')

    object_arrangement_response = to_chat_gpt(objects)

    run_segmentor(object_arrangement_response)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default= 'assets/dining1.jpg')
    parser.add_argument('--use_vqa', action='store_true', description='Tasks VQA model to provide scene/object description.')
    parser.add_argument('--objects_present', type=str, default='fork, knife, spoon, plate', description='Manually list objects seen. Separate by a comma.')
    args = parser.parse_args()
    run_main(args)