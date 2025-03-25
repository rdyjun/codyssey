def problem():
    return '화성 기지 폭발'

def reason(reason_log):
    if 'Oxygen tank unstable' in reason_log:
        return '산소 탱크 불안정'
    
    return '알 수 없는 폭발: ' + reason_log