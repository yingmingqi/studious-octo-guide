function page(max,n) {
    let result = [];
    let ls=[1,2,3,4,5,6,7,8,9,10,11,12]
    if (max<6) {
        for(var i=1;i<max+1;i++) {result.push(i)}
    }
    else if (max<13 && max>5) {
        //console.log(max+" 0=> "+n)
        for(var i=0;i<ls.length;i++) {
            let t = ls.slice(i,i+5)
            if ( n<6 )                           {result=result.concat(t);break }
            if ( t[2]==n && (n==6||n==7||n==8) ) {console.log(t,t.slice(1,4)); result=result.concat(t.slice(1,4));break }
            if ( (t.indexOf(n)>-1) && t[4]==12 ) {result=result.concat(t);break }
        }
        for(var i=result.length;i>0;i--) {if(result[i]>max){result.pop()}}
        if(result[4]<11 || result[2]<11) {result.push( "..." );result.push( max )}
        if(result[0]>1 ) {result.unshift( "..." );result.unshift( 1 )}
    }
    else {
        if      ( (n-1)>5 && (max-n)>5 ) {
            //console.log(max+" 1=>"+n)
            //[2,3,7,...,8,9,10,...,22,35,99]
            result.push( parseInt((n-1)*0.3) );
            result.push( parseInt((n-1)*0.7) );
            result.push( parseInt((n-1)) );
            result.push( "..." );
            result.push( n );
            result.push( n+1 );
            result.push( n+2 );
            result.push( "..." );
            result.push( parseInt((max-n-2)*0.3)+n+2 );
            result.push( parseInt((max-n-2)*0.7)+n+2 );
            result.push( max ) 
        }
        else if ( (n-1)<6 && (max-n)>5 && n<max) {
            //console.log(max+" 2=>"+n)
            //[1,2,3,4,5,...,99]
            for (var i=0;i<5;i++) { result.push(n+i) }
            result.push( "..." );
            result.push( max ) 
        }
        else if ( (n-1)>5 && (max-n)<6 ) {
            //console.log(max+" 3=>"+n)
            //[2,3,4,...,95,96,97,98,99]
            result.push( parseInt(n*0.3) );
            result.push( parseInt(n*0.7) );
            result.push( (n-6) );
            result.push( "..." );
            for(var i=4;i>-1;i--) { result.push(max-i) };
        }
        else {}
    }
    //result.unshift( "<" );
    //result.push( ">" );
    //if (result[1] == 1) {result.shift()}
    //if (result[result.length-2] == max) {result.pop()}
    return result
}
