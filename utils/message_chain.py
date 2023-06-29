from typing import List
from mirai import MessageChain
from mirai.models.message import Plain, At, AtAll, Face, Image, FlashImage, File, Voice, Quote, Poke

def message_chain_to_list(chain: MessageChain) -> List[str]:
    message_chain_str = []
    for item in chain:
        if isinstance(item, Plain):
            message_chain_str.append(f'[Plain] {item.text}')
        elif isinstance(item, At):
            message_chain_str.append(f'[At] {item.display}({item.target})')
        elif isinstance(item, AtAll):
            message_chain_str.append('[AtAll]')
        elif isinstance(item, Face):
            message_chain_str.append(f'[Face] {item.name}({item.face_id})')
        elif isinstance(item, Image):
            message_chain_str.append(f'[Image] {item.url}')
        elif isinstance(item, FlashImage):
            message_chain_str.append(f'[FlashImage] {item.url}')
        elif isinstance(item, File):
            message_chain_str.append(f'[File] {item.name} {item.size} {item.id}')
        elif isinstance(item, Voice):
            message_chain_str.append(f'[Voice] {item.url}')
        elif isinstance(item, Quote):
            message_chain_str.append(f'[Quote] > {item.origin}')
        elif isinstance(item, Poke):
            message_chain_str.append(f'[Poke] {item.name}')
    
    return message_chain_str