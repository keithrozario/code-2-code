package cn.biq.mn.group;

import cn.biq.mn.validation.NameField;
import cn.biq.mn.validation.NotesField;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter @Setter
public class GroupUpdateForm {

    @NotBlank
    @NameField
    private String name;

    @NotesField
    private String notes;

    @NotBlank
    private String defaultCurrencyCode;

    @NotNull
    private Integer defaultBookId;

}
