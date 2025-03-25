def main():
    with open('week-2/Mars_Base_Inventory_List.csv', 'r', encoding = 'utf-8') as inventory_list_file:
        header = inventory_list_file.readline().strip()
        inventory_list = [ value.strip() for value in inventory_list_file.readlines() ]

        print('기본 출력')
        print_inventory_list(header, inventory_list)

        # 인화성 내림차순
        desc_inventory_list = sorted(inventory_list, key=lambda v: (float(v.split(',')[4].strip()), v), reverse = True)
        
        print('인화성 내림차순 출력')
        print_inventory_list(header, desc_inventory_list)

        # 인화성 70% 이상
        top_rate_flammability = [ i for i in inventory_list if float(i.split(',')[4].strip()) >= 0.7 ]
        print('인화성이 0.7 이상인 목록 출력')
        print_inventory_list(header, top_rate_flammability)

        with open('week-2/Mars_Base_Inventory_danger.csv', 'w', encoding = 'utf-8') as danger_file:
            danger_file.write(header + '\n')
            for content in top_rate_flammability:
                danger_file.write(content + '\n')

        with open('week-2/Mars_Base_Inventory_List.bin', 'wb') as binary_file:
            binary_file.write(header.encode('utf-8') + b'\n')
            for content in desc_inventory_list:
                binary_file.write(content.encode('utf-8') + b'\n')

        with open('week-2/Mars_Base_Inventory_List.bin', 'rb') as binary_file:
            print('바이너리 파일 출력')
            print(binary_file.read().decode('utf-8'))


def print_inventory_list(header, inventory_list):
    print(header)
    for content in inventory_list:
        print(content)
    print('\n');

if __name__ == "__main__":
    try:
        main()
    except FileExistsError as e:
        print(f'이미 존재하는 파일입니다: {e}')
    except FileNotFoundError as e:
        print(f'파일이 존재하지 않습니다: {e}')
    except PermissionError as e:
        print(f'권한이 없습니다: {e}')
    except IsADirectoryError as e:
        print(f'디렉토리입니다: {e}')
    except NotADirectoryError as e:
        print(f'디렉토리가 아닙니다: {e}')
    except EOFError as e:
        print(f'EOF 에러: {e}')
    except OSError as e:
        print(f'OS 에러: {e}')
    except BlockingIOError as e:
        print(f'Blocking IO 에러: {e}')
    except Exception as e:
        print(f'알 수 없는 오류: {e}')
