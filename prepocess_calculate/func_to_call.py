import json
import re
import ast
from typing import List, Dict, Any

def parse_all_data(file_path: str) -> List[Dict[str, Any]]:
    """Парсинг всех данных без учета времени ответа"""
    return _parse_data(file_path, include_time=False)

def parse_data_with_time(file_path: str) -> List[Dict[str, Any]]:
    """Парсинг данных с сохранением времени ответа"""
    return _parse_data(file_path, include_time=True)

def _parse_data(file_path: str, include_time: bool) -> List[Dict[str, Any]]:
    """Базовая функция парсинга"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = []
    for item in data:
        parsed = {
            'selected_role': item['Выбранная роль'],
            'campus': item['Кампус'],
            'education_level': item['Уровень образования'],
            'question_category': item['Категория вопроса'],
            'user_question': _clean_text(item['Вопрос пользователя']),
            'user_filters': item['user_filters'],
            'question_filters': item['question_filters'],
            'saiga_answer': _clean_text(item['Saiga']),
            'giga_answer': _clean_text(item['Giga']),
            'winner': item['Кто лучше?'],
            'comment': item['Комментарий'],
            'contexts': _parse_contexts(item['Ресурсы для ответа'])
        }

        if item.get('Уточненный вопрос пользователя'):
            parsed.update({
                'refined_question': _clean_text(item['Уточненный вопрос пользователя']),
                'refined_answer': _clean_text(item['Ответ AI (уточнение)']),
                'refined_contexts': _parse_contexts(item['Ресурсы для ответа (уточнение)'] or '')
            })

        if include_time:
            parsed.update({
                'response_time': item['Время ответа модели (сек)'],
                'refined_response_time': item.get('Время ответа модели на уточненный вопрос (сек)')
            })
        
        result.append(parsed)
    
    return result

def _parse_contexts(resources: str) -> List[Dict[str, Any]]:
    """Парсинг контекстов с использованием вашей функции"""
    contexts = []
    pattern = re.compile(r"Document\(page_content='(.*?)', metadata=({.*?})\)", re.DOTALL)
    
    for match in re.finditer(pattern, resources):
        content, metadata_str = match.groups()
        try:
            metadata = ast.literal_eval(metadata_str)
            tags = _extract_tags(metadata)
            
            contexts.append({
                'text': _clean_text(content),
                'metadata': {
                    'source': metadata.get('source'),
                    'file_name': metadata.get('file_name'),
                    'url': metadata.get('url')
                },
                'tags': tags
            })
        except Exception as e:
            print(f"Контекст не распарсился: {e}")
    
    return contexts

def _extract_tags(metadata: Dict) -> Dict[str, List[str]]:
    """Извлечение тегов в отдельные категории"""
    return {
        'topic_tags': [v for k,v in metadata.items() if k.startswith('topic_tag_') and v],
        'user_tags': [v for k,v in metadata.items() if k.startswith('user_tag_') and v]
    }

def _clean_text(text: str) -> str:
    """Очистка текста"""
    if not text: return ''
    return re.sub(r'\\[nrt]|[\n\r\t]+|\s+', ' ', text).strip()