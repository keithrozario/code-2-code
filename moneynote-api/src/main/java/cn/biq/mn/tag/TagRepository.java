package cn.biq.mn.tag;

import cn.biq.mn.base.BaseRepository;
import cn.biq.mn.book.Book;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;


@Repository
public interface TagRepository extends BaseRepository<Tag> {

    Optional<Tag> findOneByBookAndId(Book book, Integer id);

    long countByBook(Book book);

    boolean existsByBookAndParentAndName(Book book, Tag parent, String name);

    List<Tag> findByBookAndEnableAndCanExpense(Book book, Boolean enable, Boolean canExpense);

    List<Tag> findByBookAndEnableAndCanIncome(Book book, Boolean enable, Boolean canIncome);

//    @Modifying
//    @Query("delete from Tag where book = :book")
    void deleteByBook(Book book);

    @Modifying
    @Transactional
    @Query("UPDATE Tag SET parent = NULL where parent = :tag")
    void unChildren(Tag tag);

}
