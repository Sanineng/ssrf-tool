#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <netinet/in.h>
#include <stdbool.h>

// 실제 connect 함수의 원형
typedef int (*connect_type)(int, const struct sockaddr *, socklen_t);

// connect 함수 후킹
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
    // 원래의 connect 함수 가져오기
    connect_type orig_connect = (connect_type)dlsym(RTLD_NEXT, "connect");

    // IP 주소와 포트 번호 가져오기
    char ip_address[INET_ADDRSTRLEN];
    struct sockaddr_in *saddr = (struct sockaddr_in *)addr;
    inet_ntop(AF_INET, &(saddr->sin_addr), ip_address, INET_ADDRSTRLEN);
    int port = ntohs(saddr->sin_port);

    // IP 주소와 포트 번호 출력
    printf("HTTP 요청 시 사용된 IP 주소: %s, 포트 번호: %d\n", ip_address, port);
    const char *target_ip = "127.0.0.1";
    const int target_port = 5000;

    // IP 주소와 포트 번호가 원하는 것과 같을 때 출력
    if (strcmp(ip_address, target_ip) == 0 && port == target_port){
        FILE *pidFile = fopen("/tmp/httpreqr.pid", "r");
            if (pidFile)
            {
                char pidStr[10];
                if (fgets(pidStr, sizeof(pidStr), pidFile))
                {
                    int pid = atoi(pidStr);

                    kill(pid, SIGSEGV);
                    printf("Sent SIGSEGV signal to PID %d\n", pid);
                }
                fclose(pidFile);
            }
            else
            {
                perror("Failed to open /tmp/httpreqr.pid");
            }
    }

    // 원래의 connect 함수 호출
    return orig_connect(sockfd, addr, addrlen);
}

