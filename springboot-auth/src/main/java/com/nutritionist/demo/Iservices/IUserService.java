package com.nutritionist.demo.Iservices;
import com.nutritionist.demo.Entities.User;
import java.util.Optional;


public interface IUserService {

    User register(User user);

    Optional<User> findByEmail(String email);

    User findById(Long id);
}