package cn.biq.mn.security;

import cn.biq.mn.user.User;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.Instant;

// https://stackoverflow.com/questions/7270681/utility-class-in-spring-application-should-i-use-static-methods-or-not
// https://stackoverflow.com/questions/13746080/spring-or-not-spring-should-we-create-a-component-on-a-class-with-static-meth
// https://www.jianshu.com/p/6d8c8fae1918
@Component
@RequiredArgsConstructor
public class JwtUtils {

    private final String secretKey = "rzxlszyykpbgqcflzxsqcysyhljt";

    public String createToken(User user) {
        return JWT.create().withSubject(user.getId().toString())
                .withClaim("userId", user.getId())
                .withExpiresAt(Instant.now().plus(Duration.ofDays(30))) //30天之后过期
                .sign(Algorithm.HMAC256(secretKey));
    }

    public Integer getUserId(String jwtToken) {
        JWTVerifier verifier = JWT.require(Algorithm.HMAC256(secretKey)).build();
        return verifier.verify(jwtToken).getClaim("userId").asInt();
    }

}
