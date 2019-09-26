var i = 0;
print('\n<JS> Azure Sphere JavaScript (from file)');
print('<JS> PI = '+ 22.0/7);

while(true) {
    print('<JS> loop: ' + i++);
    wait(1.0);
    if ( i > 3 ) break;
}

for (i = 0; i < 3; i++) 
    print('<JS> i = ' + i);

print('<JS> '+ new Date().toString());



