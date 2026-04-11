1.)class Main {
    static void pattern(int n){
        for(int i=1;i<=n;i++){
            for(int j=1;j<=i;j++){
           System.out.print("*");
        }
        System.out.println();
        
    }
    }

public static void main(String[]args){
    pattern(10);} }

2.)class Main {
    static int sumrec(int n){
        if(n==1){
            return 1;
        }
    return n+sumrec(n-1);}
    
    public static void main(String[] args) {
 int a=sumrec(4);
     System.out.print("sum is:" + a);
    }
}
3.)class Main {
    static void pattern2(int n){
        for(int i=n;i>=1;i--){
            for(int j=i;j>=1;j--){
           System.out.print("*");
        }
        System.out.println();
    }
    }
public static void main(String[]args){
    pattern2(8);
} 
}
4.)
class Main {
    static int fibo(int n){
        if(n==1){
            return 0;
        }
        else if(n==2)
    {
        return 1;
    }
    else{
        return fibo(n-1) + fibo(n-2);
    }
    }
public static void main(String[]args){
int series=fibo(10);
System.out.println("fibonacci series nth term: "+ series);
} 
}
5.)
class Main {
    static double fahren(double celsius){
            return (celsius*9/5)+32;
        }
public static void main(String[]args){
    double fahrenheit=fahren(37);
System.out.println( fahrenheit);
} 
}

6.)
class Main {
    public static void main(String[] args) {
        int n=8;
        int sum=0;
        for(int i=1;i<=10;i++)
        {
            sum+=n*i; }
        System.out.println(sum);
    }
}
7.)
class Main {
    public static void main(String[] args) {
        float[] arr1={80.6f,75.3f,45.2f,95.7f,99f};
        float sum=0;
        for(float element:arr1){
            sum+=element;
        }
        System.out.println(sum);
    }
}
8.)
class Main {
    public static void main(String[] args) {
        float[] arr1={80.6f,32.4f,75.4f,99.3f,95f};
    float num=97.3f;
   boolean isInArray=false;
        for(float element:arr1){
           if(num==element){
            isInArray=true;
            break;}
        }
            if(isInArray){
                System.out.println("FOUND");
            }
        else{
            System.out.println("NOT FOUND");
        }
    }
}
9.)
class Main {
    public static void main(String[] args) {
        float[] phyMarks={80.6f,32.4f,75.4f,99.3f,95f};
        float sum=0;
        for(float element:phyMarks){
           sum+=element;}
          float avg=sum/phyMarks.length;
            System.out.println("average of phy marks: "+avg);
    }
}
10.)
class Main {
    public static void main(String[] args) {
       int [][] mat1={{2,5,4},{5,4,8}};
        int [][] mat2={{1,9,4},{5,3,6}};
        int [][] result={{0,0,0},{0,0,0}};
        for(int i=0;i<mat1.length;i++){
            for(int j=0;j<mat1[i].length;j++){
                System.out.format("setting value for i=%d and j=%d\n",i,j);
                result[i][j]=mat1[i][j]+mat2[i][j];
            }}
        for(int i=0;i<mat1.length;i++){
            for(int j=0;j<mat1[i].length;j++){
                System.out.print(result[i][j]+" ");
                result[i][j]=mat1[i][j]+mat2[i][j];
            }
            System.out.println(" ");
    }
}
}
11.)
class Main {
    public static void main(String[] args) {
        int [] arr1={5,6,7,85,10,33,88};
        int l=arr1.length;
        int n=Math.floorDiv(l,2);
        int temp;
        for(int i=0;i<n;i++){
            temp=arr1[i];
            arr1[i]=arr1[l-i-1];
            arr1[l-i-1]=temp;
             }
             for(int element:arr1) {
        System.out.println(element+" ");
    }
}}
12)
class Main {
    public static void main(String[] args) {
        int [] arr1={5,6,7,858,10,33333,88};
        int max=0;
             for(int element:arr1) {
                 if(element>max){
                     max=element;
                 }}
        System.out.println(max);
    
}}
13)
class Main {
    public static void main(String[] args) {
        int [] arr1={5,6,7,-858,10,33333,-88};
        int min=0;
             for(int element:arr1) {
                 if(element<min){
                     min=element;
                 }}
        System.out.println(min);
    
}}
14)
class Main {
    public static void main(String[] args) {
        int [] arr1={5,6,7,8,10,33,880};
        boolean isSorted=true;
        for(int i=0;i<arr1.length-1;i++){
            if(arr1[i]>arr1[i+1]){
                isSorted=false;
            }
        }
        if(isSorted){
        System.out.println("array is sorted");
        }
        else{
               System.out.println("array is not sorted");
        }
}}
15) object and classes:
class Demo {
    int a=10;
    String b="hello";
    void Show()
    {
        System.out.print(a+" "+b);
    }
}
    class Test{
    }
        public class Main{
        public static void main(String[] args) {
        Demo r=new Demo();
        r.Show();
    }
    }
16.Constructors:
class A{
    int a;
    String name;
    A(){
    a=0; 
    name="hello";
}
void show() {
    System.out.print(a+" "+name);
}
}
class B{}
    class Main{
    public static void main(String[]args){
        A r=new A();
        r.show();

}
}
 17) inheritance
class animal{
        void eat(){
            System.out.println("I AM EATING");
        }
    }
    class dog extends animal{
    }
    public class Main
    {
        public static void main(String[] args) {
        dog d=new dog();
        d.eat();
    }
    }
18. single inheritance

class animal{
       void eat(){
            System.out.println("I AM EATING");
       }    
        }
    class dog extends animal{
        void bark(){
            System.out.println("I AM BARKING");
    } 
    }
    public class Main
    {
        public static void main(String[] args) {
        animal d=new animal();
       d.eat();
       dog r1=new dog();
       r1.eat();
       r1.bark();
    }
    }
19.)multilevel inheritance
class animal{
       void eat(){
            System.out.println("I AM EATING");
       }    
        }
    class dog extends animal{
        void bark(){
            System.out.println("I AM BARKING");
    } 
    }
    class puppy extends dog{
        void walk(){
            System.out.println("I AM WALKING");
        }
    } 
    public class Main
    {
        public static void main(String[] args) {
        animal d=new animal();
       d.eat();
       dog r1=new dog();
       r1.eat();
       r1.bark();
       puppy r2=new puppy();
       r2.eat();
       r2.bark();
       r2.walk();
    }
    }
20. heirarichal in
class animal{
       void eat(){
            System.out.println("I AM EATING");
       }    
        }
    class dog extends animal{
        void bark(){
            System.out.println("I AM BARKING");
    } 
    }
    class puppy extends animal{
        void walk(){
            System.out.println("I AM WALKING");
        }
    } 
    public class Main
    {
        public static void main(String[] args) {
        animal d=new animal();
       d.eat();
       dog r1=new dog();
       r1.eat();
       r1.bark();
       puppy r2=new puppy();
       r2.eat();
       r2.walk();
    }
    }
	

