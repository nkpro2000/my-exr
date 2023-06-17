#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("Usage:\n  %s <uid> <gid> <path>\n\n", argv[0]);
        printf("   <path>        : (string) to which ownership change needed.\n");
        printf("   <uid> & <gid> : (unsigned decimals) UserID & GroupID to which\n");
        printf("                  the given path ownership is changed to.\n");
        printf("     used atoi(), so username instead of uid, sets uid to 0.\n\n");
        printf("Suid ed root:fak CHOWN\n");
        printf("  so flatpak-system-helper don't need root privilege.\n\n");
        return 1;
    }
    
    uid_t uid = atoi(argv[1]);
    gid_t gid = atoi(argv[2]);
    const char *path = argv[3];
    
    int ec = chown(path, uid, gid);
    return ec;
}

///// Suid ed shell scripting is not allowded in linux.
// https://stackoverflow.com/questions/33565729/why-do-my-setuid-root-bash-shell-scripts-not-work
// https://unix.stackexchange.com/questions/364/allow-setuid-on-shell-scripts
