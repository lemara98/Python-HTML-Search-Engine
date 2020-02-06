from django.core.paginator import Paginator

def PaginatePages(searchedFiles, N):
    p = Paginator(searchedFiles, N)
    currentPage = p.page(1)
    while True:
        for file in currentPage.object_list:
            print(file.file.name)
        pr = False
        if currentPage.has_previous():
            pr = True
            print("Prev", end=" ")
        start = 1
        end = p.num_pages
        if p.num_pages > 10:
            end = 10
            if currentPage.number > 6 :
                start = currentPage.number - 5
                end = currentPage.number + 4
                if end > p.num_pages:
                    start = start - (end - p.num_pages)
                    end = p.num_pages       #sada treba prikazati vise stranica pre ove, posto ima mesta
        for page in range(start, end):
            if page == currentPage.number:
                CRED = '\033[91m'
                CEND = '\033[0m'
                print(CRED + str(page) + CEND, end=" ")
            else:
                print(page, end=" ")
        n = False

        if currentPage.has_next():      #zeza kod poslenje stranice, pogledati sta je frka
            n = True
            print("Next")

        print("Press N to change number of files per page ")

        print("Press 0 to Exit")


        option = input("choose option")

        if option == "0":
            break
        if pr == True:
            if option == "Prev":
                currentPage = p.page(currentPage.previous_page_number())
        for i in range(1, p.num_pages):
            if option == str(i):
                currentPage = p.page(i)
                break
        if n == True:
            if option == "Next":
                currentPage = p.page(currentPage.next_page_number())

        if option == "N":
            numFiles = input("Unesite novi broj fajlova po stranici: ")
            p = Paginator(searchedFiles, numFiles)
            currentPage = p.page(1)