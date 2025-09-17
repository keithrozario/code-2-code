package cn.biq.mn.group;

import cn.biq.mn.base.IdAndNameEntity;
import cn.biq.mn.validation.NotesField;
import cn.biq.mn.book.Book;
import cn.biq.mn.user.User;
import cn.biq.mn.user.UserGroupRelation;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "t_user_group")
@Getter @Setter
public class Group extends IdAndNameEntity {

    @Column(length = 1024)
    @NotesField
    private String notes;

    @Column(nullable = false)
    @NotNull
    private Boolean enable = true;

    @ManyToOne(optional = true, fetch = FetchType.LAZY)
    private User creator;

    @OneToMany(mappedBy = "group", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private Set<UserGroupRelation> relations = new HashSet<>();

    @ManyToOne(optional = true, fetch = FetchType.LAZY)
    private Book defaultBook; //组默认操作的账本

    @Column(nullable = false, length = 8)
    @NotNull
    private String defaultCurrencyCode;//默认的币种

    public Group() { }

    public Group(Integer id) {
        super.setId(id);
    }

}
